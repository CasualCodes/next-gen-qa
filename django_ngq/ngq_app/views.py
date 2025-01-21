from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import URLForm


# Create your views here.
def index(request):
    # Setup Form Pseudocode
    #   - input 'Enter URL'
    #   - submit
    
    # Index page pseudocode (Core function)
    # # if form.is_valid():
    # - After submit, load loading widget
    # - After loading widget, run scraper->promptgenerator->llm->table_generator pipeline
    # # data = generate_table(generate_test_cases(scrape_url(url)))
    # Save data to session
    # # request.session['data'] = data
    # After running, redirect to results page with data
    # # HttpResponseRedirect('results')

    # else : 
    # Load HTML
    return HttpResponse("Hello, world. You're at the index page.")

def results(request):
    # Results Page Pseudocode
    # Receive data, if fail, show blank
    # # data = request.session['data']
    # After receiving data, load dataframe to table widget

    # Other Buttons

    # Load HTML
    return HttpResponse(f"Hello, world. You're at the results page")