## Code References
# - Microsoft Copilot advice
# - Django Documentation (Getting Started) : https://docs.djangoproject.com/en/5.1/intro/tutorial01/
# - Django Documentation (Static Files) : https://docs.djangoproject.com/en/5.1/howto/static-files/
# - Django Documentation (Request/Session) : https://docs.djangoproject.com/en/5.1/topics/http/sessions/
# - Django Documentation (Async, Uvicorn) : 

## Django Imports + Time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
import time # for checking runtime

## Imports for Tables and Download
import pandas as df
from django.template.loader import render_to_string
import pdfkit
from .forms import URLForm
from .utils import data_scrape, create_table_dataset, get_divide_indices, create_tables, divide_scraped_data, divide_llm_output, clean_url, remove_common_error, load_model_chain, get_accurate_element_count, table_prompt_generator
from .tasks_store import tasks

## Imports for asynchronous functions
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
import asyncio

## TODO : Address Two-Tab Generation / Scraping Potential Errors -> LIMITATION
## TODO : Address Internal Errors

## INDEX PAGE ##
def index(request):
    form = URLForm()
    # Index page pseudocode (Core function)
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            request.session['url'] = form.cleaned_data['url']
            return redirect("results", permanent=True)
        else :
            print(False)

    # Load HTML
    return render(request, "ngq_app/home.html", {"form": form})

## ABOUT PAGE ##
def about(request):
    return render(request, "ngq_app/about.html")

## FAQ PAGE ##
def faq(request):
    return render(request, "ngq_app/faq.html")

## DYNAMIC RESULTS PAGE ##
def results(request):
    # update_context(request)
    return render(request, "ngq_app/results.html") # , request.session['full_context']

def static_results(request):
    update_context(request)
    return render(request, "ngq_app/static_results.html", request.session['full_context']) # , request.session['full_context']

## SCRAPING PROCEDURE (ASYNCHRONOUS) ##
# Cancellation (ran through fetch)
async def cancel_scraping(request):
    # Cancel Scraping Task
    task_id = await sync_to_async(request.session.get)('task_id', default=None) # str(id(request))
    print(f"cancel_scraping {task_id}")
    try:
        tasks[task_id]['scraping_task'].cancel()
    except Exception:
        print("this error is raised from successful scraping cancellation")
    return JsonResponse({'status': 'completed'})
# Procedure Proper
async def scrape_procedure(request):
    try:
        start = time.time()
        url = await sync_to_async(request.session.get)('url', default=None)
        scraped_dataset = data_scrape(url)
        # request.session['scraped_dataset'] = data_scrape(request.session['url'])
        await sync_to_async(request.session.__setitem__)('scraped_data', scraped_dataset[0])
        # request.session['scraped_data'] = (request.session['scraped_dataset'])[0]
        await sync_to_async(request.session.__setitem__)('ids', scraped_dataset[1])
        # request.session['ids'] = (request.session['scraped_dataset'])[1]
        divided_scraped_data = divide_scraped_data(scraped_dataset[0])
        await sync_to_async(request.session.__setitem__)('divided_scraped_data', divided_scraped_data)
        #  = divide_scraped_data(request.session['scraped_data'])
        indices = get_divide_indices(divided_scraped_data)
        await sync_to_async(request.session.__setitem__)('indices', indices)
        # request.session['indices'] = get_divide_indices(request.session['scraped_data'])
        end = time.time()
        print(f"Scraping Finished In : {(end-start) * 10**3}, ms")
    except asyncio.CancelledError:
        print('scrape_procedure : cancel procedure begins')
        raise
    finally:
        print('scrape_procedure : cancel procedure ends')
# Kickstart function (ran through fetch)
async def process_data(request):
    # JSON Response
    json_response = JsonResponse({'status': 'completed'})
    # Initialize Task
    await sync_to_async(request.session.__setitem__)('task_id', str(id(request)))
    task_id = await sync_to_async(request.session.get)('task_id', default=None)
    if task_id not in tasks:
        tasks[task_id] = {}
    print(f"process_data {task_id}")
    tasks[task_id]['scraping_task'] = asyncio.create_task(scrape_procedure(request))
    # request.session['scraping_task'] = asyncio.create_task(scrape_procedure(request))
    try:
        # Start Scraping Task
        await tasks[task_id]['scraping_task']
    except asyncio.CancelledError:
        print("scrape_procedure() is successfully cancelled")
    return json_response

## UPDATE CONTEXT ##
def update_context(request):
    # Divide LLM Output
    request.session['divided_llm_output'] = divide_llm_output(request.session['llm_output'], request.session['indices'])
    request.session['undivided_llm_output'] = create_table_dataset(request.session['llm_output'], ids=request.session['ids']).to_html(table_id="results-table", index=False).replace('\\n', '<br>').replace('<thead>', '<tbody>')

    # Categories and Count
    categories = ["Button", "Link", "Header", "Paragraph", "Form Submit", "Input"]
    category_count = get_accurate_element_count(request.session['ids'], request.session['indices'], request.session['divided_scraped_data'])
    
    # Create HTML tables from dataframe
    table_category_ids = ["-buttons","-links","-headers","-paragraphs","-formsubmits","-inputs"]
    prompts = table_prompt_generator(request.session['scraped_data'], request.session['url'])
    request.session['tables'] = create_tables(request.session['divided_llm_output'], request.session['ids'], request.session['indices'], prompts) #, prompts
    i = 0
    while i < len(request.session['tables']):
        (request.session['tables'])[i] = (request.session['tables'])[i].to_html(table_id=f"table{table_category_ids[i]}", index=False).replace('\\n', '<br>').replace('<thead>', '<tbody>')
        i+=1

    ## Safe Dynamic Table Divsion
    i = 0
    div_opening = "<div class=\"table-section\" style=\"display: block;\", \"overflow-x: auto;\">" 
    request.session['dynamic_test_cases'] = ""
    while i < len(request.session['tables']):
        request.session['dynamic_test_cases'] = request.session['dynamic_test_cases'] + div_opening + f"<h2 style=\"color: white;\">{categories[i]}s : {category_count[i]}</h2>" + (request.session['tables'])[i] + "</div>"
        i+=1
        
    # Other Buttons / UI elements
    url = request.session['url']
    # from datetime import date
    # timestamp = (date.today()).strftime("%Y-%m-%d %H:%M:%S") 
    test_case_count = len(request.session['llm_output'])
    elements_count = len(request.session['scraped_data'])
    accurate_elements_count = sum(category_count)

    # Store Context
    request.session['full_context'] = {
        ## LEGACY CONTEXT / UNUSED CONTEXT
        # "test_cases_undivided" : request.session['undivided_llm_output'],
        # "timestamp" : timestamp, 
        # "test_cases" : request.session['tables'], 
        ## USED CONTEXT
        "test_cases_dynamic" : request.session['dynamic_test_cases'],
        "url" : url, 
        "test_case_count" : test_case_count, 
        "categories" : categories,
        "category_count" : category_count,
        "buttons_count" : category_count[0],
        "links_count" : category_count[1],
        "headers_count" : category_count[2],
        "paragraphs_count" : category_count[3],
        "submit_fields_count" : category_count[4],
        "input_fields_count" : category_count[5],
        "elements_count" : elements_count,
        "accurate_elements_count" : accurate_elements_count,
        }

## GENERATION PROCEDURE (ASYNCHRONOUS) ##
# Cancellation (ran through fetch)
async def cancel_generation(request):
    # Cancel Generation Task
    task_id = await sync_to_async(request.session.get)('task_id', default=None)
    print(f"cancel_generation {task_id}")
    try:
        tasks[task_id]['generation_task'].cancel()
    except Exception:
        print("this error is raised by successful generation cancellation")
    # request.session['generation_task'].cancel()
    return JsonResponse({'status': 'completed'})
# Procedure Proper
## TODO : ADDRESS MULTI TABS ARE UPDATED BY THE SAME GROUP WEBSOCKET ISSUE
async def generation_procedure(request):
    ## Asynchronous (Update Frontend) Setup
    from .consumers import cancel_flags
    channel_layer = get_channel_layer()
    session_id = request.session.session_key

    print(f"Process_Results {session_id}")
    cancel_flag = cancel_flags.get(session_id)
    group_name = "updates"

    ## Integrate Test Case Generation Code
    from .utils import template, model_str, DEBUG_SETTING
    # Load LLM Chain
    chain = load_model_chain(template, model_str)

    # Return Data
    await sync_to_async(request.session.__setitem__)('llm_output', [])
    # request.session['llm_output'] = []
    return_data = []

    scraped_data = await sync_to_async(request.session.get)('scraped_data', default=None)
    try:
        i = 0
        total = len(scraped_data)
        for item in scraped_data:
            # # Early Cancellation Attempt : First Check
            # if cancel_flag and cancel_flag.is_set():
            #     print("Processing Scraped Data is Cancelled Early")
            #     break

            test_case = chain.invoke({"ui_element": str(item), "url": request.session['url']})
            test_case = str(remove_common_error(test_case))

            # # Early Cancellation Attempt : Final Check
            # if cancel_flag and cancel_flag.is_set():
            #     print("Processing Scraped Data is Cancelled Early")
            #     break

            # Update LLM_Output
            return_data.append(test_case)
            # print(len(return_data))
            await sync_to_async(request.session.__setitem__)('llm_output', return_data)
            # out = await sync_to_async(request.session.get)('llm_output', default=None)
            # print(len(out))
            # request.session['llm_output'].append(test_case)
            update_context(request)
            updated_context = await sync_to_async(request.session.get)('full_context', default=None)
            # Update Frontend
            await channel_layer.group_send(group_name,
                {
                    "type": "update_message",
                    "context": updated_context,
                }
            )

            # LLM Reset To Free Up Context
            chain = load_model_chain(template, model_str)
            if (DEBUG_SETTING == 1):
                print(f"test case {i} out of {total} generated")
            i += 1
            if i == 10:
                break
    except asyncio.CancelledError:
        print('generation_procedure : cancel procedure begins')
        raise
    finally:
        print('generation_procedure : cancel procedure ends')
# Kickstart function (ran through fetch)
async def process_results(request):
    # JSON Response
    json_response = JsonResponse({"status": "completed"})
    await sync_to_async(request.session.__setitem__)('task_id', str(id(request)))
    task_id = await sync_to_async(request.session.get)('task_id', default=None)
    print(f"process_results {task_id}")
    if task_id not in tasks:
        tasks[task_id] = {}
    tasks[task_id]['generation_task'] = asyncio.create_task(generation_procedure(request))
    # request.session['generation_task'] = asyncio.create_task(generation_procedure(request))
    try:
        # Start Scraping Task
        await tasks[task_id]['generation_task']
    except asyncio.CancelledError:
        print("generation_procedure() is successfully cancelled")
    return json_response

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

# ## LOADING PAGE ##
# def loading(request):
#     # Javascript in loading.html does the threading
#     return render(request, "ngq_app/loading.html")
# ## LOADING RESULTS ##
# def loading_results(request):
#     return render(request, "ngq_app/loading_results.html")