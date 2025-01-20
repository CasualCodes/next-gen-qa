from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index():
    # Setup Form Pseudocode
    #   - input 'Enter URL'
    #   - submit
    
    # Index page pseudocode (Core function)
    # After submit, load loading widget
    # After loading widget, run scraper->promptgenerator->llm->table_generator pipeline
    # After running, redirect to results page with data

    # Load HTML
    return HttpResponse("Hello, world. You're at the index page.")

def results(data):
    # Results Page Pseudocode
    # Receive data, if fail, show blank
    # After receiving data, load dataframe to table widget

    # Other Buttons

    # Load HTML
    return HttpResponse(f"Hello, world. You're at the results page")