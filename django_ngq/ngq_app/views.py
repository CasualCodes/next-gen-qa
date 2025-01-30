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
    # Setup Form Pseudocode
    #   - input 'Enter URL'
    #   - submit
    form = URLForm()
    
    # Index page pseudocode (Core function)
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            print(True)
            # print(form.cleaned_data['url'])
            request.session['url'] = form.cleaned_data['url']
            return redirect("loading", permanent=True)
        else :
            print(False)

    # else : 
    # Load HTML
    return render(request, "ngq_app/home.html", {"form": form})

def loading(request):
    # TODO : Threading
    # - After submit, load loading widget
    # - After loading widget, run scraper->promptgenerator->llm->table_generator pipeline
    # # data = generate_table(generate_test_cases(scrape_url(url)))
    # Save data to session
    # # request.session['data'] = data
    # After running, redirect to results page with data
    # # HttpResponseRedirect('results')
    return render(request, "ngq_app/loading.html")

def process_data(request):
    DEBUG = 1

    if (DEBUG == 0):
        time.sleep(10)
        request.session['test_cases'] = 0
        
    elif (DEBUG == 1):
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
    # Results Page Pseudocode
    # Receive data, if fail, show blank
    # # data = request.session['data']
    # After receiving data, load dataframe to table widget

    # Other Buttons

    # Load HTML
    # print(request.session['llm_output'])
    request.session['test_cases'] = create_table_dataset(request.session['llm_output'])
    request.session['test_cases'] = request.session['test_cases'].to_html()
    test_cases = request.session['test_cases']
    return render(request, "ngq_app/results.html", {"test_cases" : test_cases})