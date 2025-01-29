from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import URLForm
from .utils import data_scrape, dataframe_init, create_table_dataset, load_model_chain, create_test_cases, csv_from_test_case_batches

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

def results(request):
    # Results Page Pseudocode
    # Receive data, if fail, show blank
    # # data = request.session['data']
    # After receiving data, load dataframe to table widget

    # Other Buttons

    # Load HTML
    return render(request, "ngq_app/results.html")