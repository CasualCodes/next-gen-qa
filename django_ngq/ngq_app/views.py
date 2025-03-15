from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
import pandas as df
import time # for checking runtime
from django.template.loader import render_to_string
import pdfkit

from .forms import URLForm
from .utils import data_scrape, create_table_dataset, create_test_cases, get_divide_indices, create_tables, divide_scraped_data, divide_llm_output, clean_url

## INDEX PAGE ##
def index(request):
    form = URLForm()
    # Index page pseudocode (Core function)
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            request.session['url'] = form.cleaned_data['url']
            return redirect("loading", permanent=True)
        else :
            print(False)

    # Load HTML
    return render(request, "ngq_app/home.html", {"form": form})

## LOADING PAGE ##
def loading(request):
    # Javascript in loading.html does the threading
    return render(request, "ngq_app/loading.html")

# Loaded by javascript asynchronously during loading screen
def process_data(request):
    start = time.time()
    request.session['scraped_dataset'] = data_scrape(request.session['url'])
    request.session['scraped_data'] = (request.session['scraped_dataset'])[0]
    request.session['ids'] = (request.session['scraped_dataset'])[1]
    request.session['indices'] = get_divide_indices(request.session['scraped_data'])
    end = time.time()
    print(f"Scraping Finished In : {(end-start) * 10**3}, ms")

    start = time.time()
    request.session['llm_output'] = create_test_cases(data=request.session['scraped_data'], url=request.session['url'])
    end = time.time()
    print(f"Generation Finished In : {(end-start) * 10**3}, ms")

    return JsonResponse({'status': 'completed'})

## RESULTS PAGE ##
def results(request):
    # Divide LLM Output
    request.session['divided_llm_output'] = divide_llm_output(request.session['llm_output'], request.session['indices'])

    # Create HTML tables from dataframe
    categories = ["Button", "Link", "Header", "Paragraph", "Form Submit", "Input"]
    request.session['tables'] = create_tables(request.session['divided_llm_output'], request.session['ids'], request.session['indices'])
    i = 0
    while i < len(request.session['tables']):
        (request.session['tables'])[i] = (request.session['tables'])[i].to_html(table_id="results-table", index=False).replace('\\n', '<br>')
        i+=1

    # OPTIONAL TODO : Determine if this is suitable for website rendering too
    request.session['no_header'] = create_tables(request.session['divided_llm_output'], request.session['ids'], request.session['indices'])
    i = 0
    while i < len(request.session['no_header']):
        (request.session['no_header'])[i] = (request.session['no_header'])[i].to_html(table_id="results-table", index=False).replace('\\n', '<br>').replace('<thead>', '<tbody>')
        i+=1
        
    # Other Buttons / UI elements
    url = request.session['url']
    from datetime import date
    timestamp = (date.today()).strftime("%Y-%m-%d %H:%M:%S") 
    test_case_count = len(request.session['llm_output'])
    category_count = []
    for category in divide_scraped_data(request.session['scraped_data']):
        category_count.append(len(category))

    # Store Context for printing pdf
    # OPTIONAL TODO : Consider using this as context
    request.session['full_context'] = {"test_cases" : request.session['no_header'], 
                   "url" : url, 
                   "timestamp" : timestamp, 
                   "test_case_count" : test_case_count, 
                   "categories" : categories,
                   "category_count" : category_count,
                    }

    # Load HTML. load dataframe to table widget
    return render(request, "ngq_app/results.html", 
                  {"test_cases" : request.session['tables'], 
                   "url" : url, 
                   "timestamp" : timestamp, 
                   "test_case_count" : test_case_count, 
                   "categories" : categories,
                   "category_count" : category_count,
                   })

## DOWNLOAD ##
# Download CSV
def download(request):
    filename = clean_url(request.session['url'])
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
    create_table_dataset(request.session['llm_output'], ids=request.session['ids']).to_csv(index=False, header=True, path_or_buf=response)
    return response
# Download PDF (using pdfkit and wkhtmltopdf)
def download_pdf(request):
    filename = clean_url(request.session['url'])
    pdf = render_to_string(template_name='ngq_app/pdf_template.html', context=request.session['full_context'])
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'no-outline': None
    }
    pdf = pdfkit.from_string(pdf, False, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
    return response