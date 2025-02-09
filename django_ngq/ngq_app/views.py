from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
import pandas as df
import time # for checking runtime

from .forms import URLForm
from .utils import data_scrape, create_table_dataset, create_test_cases

# Create your views here
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

def loading(request):
    # Javascript in loading.html does the threading
    return render(request, "ngq_app/loading.html")

# Loaded by javascript asynchronously during loading screen
def process_data(request):
    start = time.time()
    scraped_data = data_scrape(request.session['url']) 
    end = time.time()
    print(f"Scraping Finished In : {(end-start) * 10**3}, ms")

    start = time.time()
    request.session['llm_output'] = create_test_cases(scraped_data)
    end = time.time()
    print(f"Generation Finished In : {(end-start) * 10**3}, ms")

    return JsonResponse({'status': 'completed'})

def results(request):
    # Receive data, if fail, show blank
    request.session['test_cases'] = create_table_dataset(request.session['llm_output'])
    request.session['test_cases'] = request.session['test_cases'].to_html(table_id="results-table", index=False)
    test_cases = request.session['test_cases']
    
    # Other Buttons / UI elements
    url = request.session['url']
    from datetime import date
    timestamp = date.today()
    test_case_count = len(request.session['llm_output'])

    # Load HTML. load dataframe to table widget
    return render(request, "ngq_app/results.html", {"test_cases" : test_cases, "url" : url, "timestamp" : timestamp, "test_case_count" : test_case_count})

def download(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="test_cases.csv"'
    create_table_dataset(request.session['llm_output']).to_csv(encoding='utf-8', index=False, header=True, path_or_buf=response)
    return response