## UTILS.PY ##
# - consists of the main components of the pipeline
# Scraper -> Prompt Generator (+ LLM) -> Table Generator

## Scraper
from selenium import webdriver

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

# Setup driver
def setup_driver():
    try :
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options) # Default with Firefox
    except Exception:
        try : 
            driver = webdriver.Chrome() # Default with Chrome            
            ## driver = webdriver.Chrome(options=options)

            ## Uncomment when setting up for gcolab (and using chrome)
            # from selenium.webdriver import ChromeOptions
            # from selenium.webdriver.chrome.service import Service
            # from webdriver_manager.chrome import ChromeDriverManager
            # from selenium.webdriver.chrome.options import Options
            # import google_colab_selenium as gs
            # options = ChromeOptions()
            # options.add_argument("--headless")
            # driver = gs.Chrome()
        except Exception:
            try : 
                options = webdriver.EdgeOptions()
                options.add_argument("--no-sandbox")
                options.add_argument("--headless")
                driver = webdriver.Edge(options=options) # Default with Edge
            except Exception:
                print("Error. No usable browser found for scraping")
    
    return driver

# Data Scraper: Returns list of scraped elements and test case ids for each element.
def data_scrape(url):
    driver = setup_driver()
    data = []
    ids = []
    driver.get(url)

    i = 1

    # BUTTONS
    buttons = driver.find_elements(By.CSS_SELECTOR, "button")
    for button in buttons:
        if button.is_displayed():
            # Button Element Attributes
            button_text = f"Button Element '{button.text}'" if (button.text != None and button.text != "") else "Button Element Without Name (might be an image)"
            button_size = f"With Size Attribute {button.size}" if button.size != None else ""
            button_color = f"With Color Attribute {button.value_of_css_property("color")}" if button.value_of_css_property("color") != None else ""
            button_background_color = f"With Background Color Attribute {button.value_of_css_property("background-color")}" if button.value_of_css_property("background-color") != None else ""
            button_enabled = "Clickable" if button.is_enabled() else "Not Clickable"
            
            j = 0
            # Store Button Element
            store_clickability = f"{button_enabled} {button_text}"
            data.append(store_clickability)
            ids.append(f"{i}.{j}")
            if (button_color != "" or button_background_color != ""):
                store_color = f"{button_text} {button_color} {button_background_color} "
                data.append(store_color)
                j+=1
                ids.append(f"{i}.{j}")
            if (button_size != ""):
                store_size = f"{button_text} {button_size}"
                data.append(store_size)
                j+=1
                ids.append(f"{i}.{j}")
            i+=1

    ## LINKS  
    links = driver.find_elements(By.TAG_NAME,"a")
    for link in links:
        if link.is_displayed():
            # Link Element Attributes
            link_text = f"Link Element '{link.text}'" if (link.text != None and link.text != "") else "Link Element Without Name (might be an image)"
            link_url = f"With URL {link.get_attribute('href')}" if link.get_attribute('href') != None else "Without URL"
            # Additional Attributes
            link_rel = f"With rel attribute {link.get_attribute('rel')}" if link.get_attribute('rel') != None and link.get_attribute('rel') != "" else ""
            link_target = f"With target attribute {link.get_attribute('target')}" if link.get_attribute('target') != None and link.get_attribute('target') != "" else ""
            link_download = f"A download is attached to document {link.get_attribute('download')}" if link.get_attribute('download') != None and link.get_attribute('download') != "" else ""
            
            j = 0
            # Store Link Element
            store_navigation = f"{link_text} {link_url} {link_target} {link_rel}"
            data.append(store_navigation)
            ids.append(f"{i}.{j}")
            if link_download != "":
                store_download = f"{link_text} {link_download}"
                data.append(store_download)
                j+=1
                ids.append(f"{i}.{j}")
            i+=1

    # TEXT
    # Heading Elements
    for level in range(1, 7):  # HTML has 6 levels of headings (h1 to h6)
        headings = driver.find_elements(By.TAG_NAME,f"h{level}")
        for heading in headings:
            if heading.is_displayed():
                
                text_color = f"With Color {heading.value_of_css_property("color")}" if heading.value_of_css_property("color") != None else ""
                text_background_color = f"With Background Color {heading.value_of_css_property("background-color")}" if heading.value_of_css_property("background-color") != None else ""
                store = f"Heading Element (h{level}): '{heading.text}'"
                
                j = 0
                # Store
                data.append(store)
                ids.append(f"{i}.{j}")
                if (text_color != "" or text_background_color != ""):
                    data.append(f"{store} {text_color} {text_background_color}")
                    j+=1
                    ids.append(f"{i}.{j}")
                i+=1

    # Paragraph Elements
    paragraphs = driver.find_elements(By.TAG_NAME,"p")
    for paragraph in paragraphs:
        if paragraph.is_displayed():
            
            text_color = f"With Color {paragraph.value_of_css_property("color")}" if paragraph.value_of_css_property("color") != None else ""
            text_background_color = f"With Background Color {paragraph.value_of_css_property("background-color")}" if paragraph.value_of_css_property("background-color") != None else ""
            store = f"Paragraph Element: '{paragraph.text}'"

            j = 0
            # Store
            data.append(store)
            ids.append(f"{i}.{j}")
            if (text_color != "" or text_background_color != ""):
                data.append(f"{store} {text_color} {text_background_color}")
                j+=1
                ids.append(f"{i}.{j}")
            i+=1

    # Input Elements
    input_tags = driver.find_elements(By.TAG_NAME,"input")
    for input_tag in input_tags:
        if input_tag.is_displayed():
            # Basic Attributes
            input_field_name = f"Input Field Element: '{input_tag.get_attribute('name')}'" if input_tag.get_attribute('name') != None else "Without Name"
            input_field_type = f"With Type {input_tag.get_attribute('type')}" if input_tag.get_attribute('name') != None else "Without Type"
            # Additional Attributes
            input_field_value = f"With Value {input_tag.get_attribute('value')}" if input_tag.get_attribute('name') != None else "Without Value"
            input_field_placeholder = f"With Placeholder '{input_tag.get_attribute('placeholder')}'" if input_tag.get_attribute('name') != None else "Without Placeholder"
            input_field_readonly = f"Is Readonly" if input_tag.get_attribute('readonly') != None else "Is Editable"
            input_field_disabled = f"Disabled" if input_tag.get_attribute('disabled') != None else "Enabled"
            input_field_required = f"Is Required" if input_tag.get_attribute('required') != None else "Not Required"
            input_field_autocomplete = f"Is Autocomplete" if input_tag.get_attribute('autocomplete') != None else "Not Autocomplete"

            # Store based on type
            if (input_tag.get_attribute('type') == "submit"):
                store = f"Form Submit Button Element: {input_tag.get_attribute("name")} {input_field_disabled}"
                data.append(store)
                j = 0
                ids.append(f"{i}.{j}")
            else:
                store = f"{input_field_disabled} {input_field_name} {input_field_type} {input_field_required}"
                data.append(store)
                j = 0
                ids.append(f"{i}.{j}")

                store_value = f"{input_field_name} {input_field_type} {input_field_value}"
                data.append(store_value)
                j+=1
                ids.append(f"{i}.{j}")

                store_placeholder = f"{input_field_name} {input_field_type} {input_field_placeholder}"
                data.append(store_placeholder)
                j+=1
                ids.append(f"{i}.{j}")

                store_readonly = f"{input_field_name} {input_field_type} {input_field_readonly}"
                data.append(store_readonly)
                j+=1
                ids.append(f"{i}.{j}")

                store_autocomplete = f"{input_field_name} {input_field_type} {input_field_autocomplete}"
                data.append(store_autocomplete)
                j+=1
                ids.append(f"{i}.{j}")
            i+=1
            
    # Close the browser
    driver.quit()

    data = [data, ids]

    return data

# Divide Scraped Data
def divide_scraped_data(scraped_data):
    divided_scraped_data = []
    
    # Initiate titles
    category_titles = [
        "Button Element",
        "Link Element",
        "Heading Element",
        "Paragraph Element",
        "Form Submit Button Element",
        "Input Field Element"
    ]

    # Inititate sublists
    buttons = []
    links = []
    headers = []
    paragraphs = []
    form_submits = []
    inputs = []

    # Initiate mainlist
    divided_scraped_data = [
        buttons,
        links,
        headers,
        paragraphs,
        form_submits,
        inputs
    ]

    i = 0
    while (i < len(scraped_data)):
        # Check through titles
        for title in category_titles:
            if (title in scraped_data[i]):
                divided_scraped_data[category_titles.index(title)].append(scraped_data[i])
                break
        i+=1

    return divided_scraped_data


# Get divide indices based on scraped data for llm output division
def get_divide_indices(scraped_data):
    divided_scraped_data = divide_scraped_data(scraped_data)
    indices = []

    i = 0
    for data_type in divided_scraped_data:
        indices.append(i)
        for data in data_type:
            i+=1

    return indices

## Prompt Generator + LLM
# Langchain and Ollama
import langchain
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

TEMPLATE_SETTING = 0
DEBUG_SETTING = 1

# Template Setting. Detailed format for non-fine-tuned. Simplified format for fine-tuned.
if (TEMPLATE_SETTING == 0):
    # Template for non fine tuned model
    # CONTEXT V3
    template = """You are an expert in software quality assurance specializing in usability testing.

    Consider the following usability aspects:
    Accessibility (keyboard navigation, screen reader support, etc.)
    Responsiveness (behavior across different screen sizes, etc.)
    Feedback (hover effects, click responses, error messages, etc.)
    Interactivity (expected behavior when clicked, typed into, or focused, etc.)
    User experience (clarity of labels, ease of use, etc.)

    Avoid descriptions like "The user" or "The test participant" and should instead focus on direct, executable actions.

    Given this UI Element: {ui_element}
    From this website: {url}

    Generate a functional usability test case with the following aspects, separated by a `~`:
    - **Objective**: Clearly state the objective of the test.
    - **Preconditions**: List any preconditions that need to be met.
    - **Test Steps**: Provide a step-by-step guide for the test. Each step should be a direct command, not a description.
    - **Expected Output**: Describe the expected output.

    Output format example, start with the objective directly and avoid saying "here is the test case" or the name of the testcase and end the output after writing the expected output:
    Objective: [Describe the objective] 
    ~ Preconditions: [List preconditions, use dashes] 
    ~ Test Steps: [Step-by-step guide] 
    ~ Expected Output: [Describe the expected output, use dashes]"""

    model_str = "llama3.1"
elif (TEMPLATE_SETTING == 1):
    # template and model for fine-tuned version
    template = """{ui_element} from the website: {url}"""
    model_str = "qallama"

# Remove common errors in format
def remove_common_error(output : str, setting : int = 0):
    if (setting == 0 or setting == 2):
        # Errors are strings that commonly appear as errors in the intended output
        errors = ["Objective~Preconditions~Test Steps~Expected Result", 
                "Objective:", "**Objective**:",
                "Preconditions:", "**Preconditions**:",
                "Test Steps:", "**Test Steps**:",
                "Expected Output:", "**Expected Output**:",
                "**** ", "****"
                ]
        for error in errors:
            output = output.replace(error, "")
    if (setting == 1 or setting == 2):
        # Adjustments are strings that are not intended to be deleted, but instead adjusted
        adjustments = ["Preconditions~", "Test Steps~", "Expected Result~"]
        for adjustment in adjustments:
            output = output.replace(adjustment, "~")
    return output

# Load LLM Model
def load_model_chain(template : str =  template, model_str : str = model_str, temperature=0):
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model=model_str, temperature=temperature)
    chain = prompt | model
    return chain

# Create Test cases
def create_test_cases(data, model_str : str = model_str , template : str = template, url : str = "placeholder"):
    
    # Load LLM Chain
    chain = load_model_chain(template, model_str)

    # Return Data
    return_data = []
    
    i = 0
    total = len(data)
    for item in data:
        test_case = chain.invoke({"ui_element": str(item), "url": url})
        test_case = remove_common_error(test_case)
        # OPTIONAL TODO : Add error checkers. Might be risky due to indices. So optional
        return_data.append(test_case)
        # LLM Reset To Free Up Context
        chain = load_model_chain(template, model_str)
        if (DEBUG_SETTING == 1):
            print(f"test case {i} out of {total} generated")
        i += 1

    return return_data

# Divide LLM output by element types, based on scraped data indices
def divide_llm_output(llm_output, indices):

    # Inititate sublists
    buttons = []
    links = []
    headers = []
    paragraphs = []
    form_submits = []
    inputs = []

    # Initiate mainlist
    divided_data = [
        buttons,
        links,
        headers,
        paragraphs,
        form_submits,
        inputs
    ]

    i = 0
    j = 0
    n = 0
    
    index = 0
    k = 0
    while (index < len(indices)-1):
        i = indices[index]
        j = indices[index+1]
        while (n >= i and n < j):
            divided_data[k].append(llm_output[n])
            n+=1
        k += 1
        index += 1
    while (n<len(llm_output)):
        divided_data[k].append(llm_output[n])
        n+=1
    
    return divided_data

## Table Generator
# Pandas
import pandas as pd

# Table Dataframe Initialization
def dataframe_init(data):
    df = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in data.items()]))
    return df

# CSV Generator
def csv_from_test_case_batches(filename, data):
    cols = dataframe_init(data)
    cols.to_csv(f"{filename}.csv", sep='\t', encoding='utf-8', index=False, header=True)

# Create table dataset
def create_table_dataset(llm_output, ids : list, saved_index : int = 0):

    id = []
    objective = []
    precondition = []
    test_steps = []
    expected_result = []
    actual_result = []

    i = saved_index
    for test_case in llm_output:
        split_test_case = test_case.split('~')
        
        # Validate and skip if split is a failure
        if len(split_test_case) == 4:
            # Test Case ID
            id.append(ids[i])
            # Test Case Objective
            objective.append(split_test_case[0])
            # Test Case Precondition
            precondition.append(split_test_case[1])
            # Test Case Steps 
            test_steps.append(split_test_case[2])
            # Test Case Expected Output
            expected_result.append(split_test_case[3])
            # Test Case Actual Result
            actual_result.append("Pass/Fail")

        i+=1

    data = {"Test Case ID" : id,
            "Objective" : objective,
            "Precondition" : precondition,
            "Test Steps" : test_steps,
            "Expected Result" : expected_result,
            "Actual Result" : actual_result}

    return dataframe_init(data)

# Create multiple tables
def create_tables(divided_llm_output, ids, indices):
    tables = []
    i = 0

    for llm_output in divided_llm_output:
        tables.append(create_table_dataset(llm_output, ids, indices[i]))
        i+=1

    return tables

# Find common unaccepted filename chracters / url articles and delete them
def clean_url(url : str):
    articles = ['https', 'www', ':', '/', '\\', '*', '?', '<', '>', '|', '.']
    for article in articles:
        url = url.replace(article, '')
    return url