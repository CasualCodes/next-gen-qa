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
from .utils import data_scrape, create_table_dataset, get_divide_indices, create_tables, divide_scraped_data, divide_llm_output, clean_url, remove_common_error, load_model_chain

## Code References
# - Microsoft Copilot advice
# - Django Documentation (Getting Started) : https://docs.djangoproject.com/en/5.1/intro/tutorial01/
# - Django Documentation (Static Files) : https://docs.djangoproject.com/en/5.1/howto/static-files/
# - Django Documentation (Request/Session) : https://docs.djangoproject.com/en/5.1/topics/http/sessions/

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

## PROCESS DATA ##
def process_data(request):
    start = time.time()
    request.session['scraped_dataset'] = data_scrape(request.session['url'])
    request.session['scraped_data'] = (request.session['scraped_dataset'])[0]
    request.session['ids'] = (request.session['scraped_dataset'])[1]
    request.session['indices'] = get_divide_indices(request.session['scraped_data'])
    end = time.time()
    print(f"Scraping Finished In : {(end-start) * 10**3}, ms")
    return JsonResponse({'status': 'completed'})

## UPDATE CONTEXT ##
def update_context(request):
    # Divide LLM Output
    request.session['divided_llm_output'] = divide_llm_output(request.session['llm_output'], request.session['indices'])
    request.session['undivided_llm_output'] = create_table_dataset(request.session['llm_output'], ids=request.session['ids']).to_html(table_id="results-table", index=False).replace('\\n', '<br>').replace('<thead>', '<tbody>')

    # Create HTML tables from dataframe
    categories = ["Button", "Link", "Header", "Paragraph", "Form Submit", "Input"]
    request.session['tables'] = create_tables(request.session['divided_llm_output'], request.session['ids'], request.session['indices'])
    i = 0
    while i < len(request.session['tables']):
        (request.session['tables'])[i] = (request.session['tables'])[i].to_html(table_id="results-table", index=False).replace('\\n', '<br>').replace('<thead>', '<tbody>')
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
    request.session['full_context'] = {
        "test_cases" : request.session['tables'], 
        "test_cases_undivided" : request.session['undivided_llm_output'],
        "url" : url, 
        "timestamp" : timestamp, 
        "test_case_count" : test_case_count, 
        "categories" : categories,
        "category_count" : category_count,
        }

## LOADING RESULTS ##
def loading_results(request):
    return render(request, "ngq_app/loading_results.html")

import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def process_results(request):
    ## Integrate Test Case Generation
    channel_layer = get_channel_layer()
    group_name = "updates"
    from .utils import template, model_str, DEBUG_SETTING

    # Load LLM Chain
    chain = load_model_chain(template, model_str)

    # Return Data
    request.session['llm_output'] = []
    
    i = 0
    total = len(request.session['scraped_data'])
    for item in request.session['scraped_data']:
        test_case = chain.invoke({"ui_element": str(item), "url": request.session['url']})
        test_case = remove_common_error(test_case)

        print(test_case)
        request.session['llm_output'].append(test_case)
        print(request.session['llm_output'])
        update_context(request)                    
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "update_message",
                "context": request.session['full_context'],
            }
        )
        
        # LLM Reset To Free Up Context
        chain = load_model_chain(template, model_str)
        if (DEBUG_SETTING == 1):
            print(f"test case {i} out of {total} generated")
        i += 1

    return JsonResponse({"status": "completed"})

## RESULTS PAGE ##
def results(request):
    update_context(request)
    return render(request, "ngq_app/results.html", request.session['full_context'])

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