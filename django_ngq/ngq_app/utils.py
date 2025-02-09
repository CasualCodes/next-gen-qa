## Scraper
from selenium import webdriver

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

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

def data_scrape(url):
    driver = setup_driver()
    data = []
    driver.get(url)

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
            
            # Store Button Element
            store_clickability = f"{button_enabled} {button_text}"
            data.append(store_clickability)
            if (button_color != "" or button_background_color != ""):
                store_color = f"{button_text} {button_color} {button_background_color} "
                data.append(store_color)
            if (button_size != ""):
                store_size = f"{button_text} {button_size}"
                data.append(store_size)

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
            
            # Store Link Element
            store_navigation = f"{link_text} {link_url} {link_target}"
            data.append(store_navigation)
            if link_rel != "":
                store_rel = f"{link_text} {link_rel}"
                data.append(store_rel)
            if link_download != "":
                store_download = f"{link_text} {link_download}"
                data.append(store_download)

    # TEXT
    # Heading Elements
    for level in range(1, 7):  # HTML has 6 levels of headings (h1 to h6)
        headings = driver.find_elements(By.TAG_NAME,f"h{level}")
        for heading in headings:
            if heading.is_displayed():
                
                text_color = f"With Color {heading.value_of_css_property("color")}" if heading.value_of_css_property("color") != None else ""
                text_background_color = f"With Background Color {heading.value_of_css_property("background-color")}" if heading.value_of_css_property("background-color") != None else ""
                store = f"Heading Element (h{level}): '{heading.text}'"
                
                # Store
                data.append(store)
                if (text_color != "" or text_background_color != ""):
                    data.append(f"{store} {text_color} {text_background_color}")

    # Paragraph Elements
    paragraphs = driver.find_elements(By.TAG_NAME,"p")
    for paragraph in paragraphs:
        if paragraph.is_displayed():
            
            text_color = f"With Color {paragraph.value_of_css_property("color")}" if paragraph.value_of_css_property("color") != None else ""
            text_background_color = f"With Background Color {paragraph.value_of_css_property("background-color")}" if paragraph.value_of_css_property("background-color") != None else ""
            store = f"Paragraph Element: '{paragraph.text}'"

            # Store
            data.append(store)
            if (text_color != "" or text_background_color != ""):
                    data.append(f"{store} {text_color} {text_background_color}")

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
            else:
                store = f"{input_field_disabled} {input_field_name} {input_field_type} {input_field_required}"
                data.append(store)
                store_value = f"{input_field_name} {input_field_type} {input_field_value}"
                data.append(store_value)
                store_placeholder = f"{input_field_name} {input_field_type} {input_field_placeholder}"
                data.append(store_placeholder)
                store_readonly = f"{input_field_name} {input_field_type} {input_field_readonly}"
                data.append(store_readonly)
                store_autocomplete = f"{input_field_name} {input_field_type} {input_field_autocomplete}"
                data.append(store_autocomplete)
            
    # Close the browser
    driver.quit()

    return data

## Prompt Generator + LLM
# Langchain and Ollama
import langchain
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

TEMPLATE_SETTING = 0

if (TEMPLATE_SETTING == 0):
    # Template for non fine tuned model
    # CONTEXT V2
    template = """
    You are an expert in software quality assurance specializing in usability testing. Given a UI element, generate a set of functional usability test cases with detailed test scenarios.

    The UI element could be a button, link, text, or input field (some elements have a link attached to them). Consider the attribute attached to the UI element as the attribute acts as a hint about the primary focus of the test case. Also consider the following usability aspects:

    Accessibility (keyboard navigation, screen reader support, etc.)
    Responsiveness (behavior across different screen sizes, etc.)
    Feedback (hover effects, click responses, error messages, etc.)
    Interactivity (expected behavior when clicked, typed into, or focused, etc.)
    User experience (clarity of labels, ease of use, etc.)

    Only output the following, separated by a ~:

    Objective (What the test aims to verify)
    Preconditions (Any setup or conditions required before testing)
    Test Steps (Step-by-step actions to perform the test)
    Expected Result (Expected outcome if the UI element works correctly)

    Your output should only be in the following structured format but do not include the format in the output: "Objective"~"Preconditions"~"Test Steps"~"Expected Result"
    DO NOT output anything else but one test case in the said format.

    Here is the UI Element: {ui_element}
    The UI Element is from the following website URL : {url}
    """

    model_str = "llama3.1"
elif (TEMPLATE_SETTING == 1):
    # template and model for fine-tuned version
    template = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    ### Instruction:
    Generate a test case for the following UI Element:

    ### Input:
    {question}

    ### Response: """

    model_str = "llama3.1testcase"

common_error = "Objective~Preconditions~Test Steps~Expected Result"

def load_model_chain(template : str =  template, model_str : str = "llama3.1", temperature=0.1):
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model=model_str, temperature=temperature)
    chain = prompt | model
    return chain

def create_test_cases(data, model_str : str = "llama3.1" , template : str = template, url : str = "placeholder", common_error : str = common_error):
    
    # Load LLM Chain
    chain = load_model_chain(template, model_str)

    # Return Data
    return_data = []
    
    i = 0
    total = len(data)
    for item in data:
        return_data.append(chain.invoke({"ui_element": str(item), "url": url}).replace(common_error, ""))
        # LLM Reset To Free Up Context
        chain = load_model_chain(template, model_str)
        print(f"test case {i} out of {total} generated")
        i += 1

    return return_data

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

# System Proper Parameters
def create_table_dataset(llm_output):
    id = []
    objective = []
    precondition = []
    test_steps = []
    expected_result = []
    actual_result = []

    i = 0
    for test_case in llm_output:
        split_test_case = test_case.split('~')

        # Test Case ID
        id.append(i+1)

        # Test Case Objective
        try:
            objective.append(split_test_case[0])
        except Exception:
            objective.append('error')

        # Test Case Precondition
        try:
            precondition.append(split_test_case[1])
        except Exception:
            precondition.append('error')

        # Test Case Steps 
        try:
            test_steps.append(split_test_case[2])
        except Exception:
            test_steps.append('error')

        # Test Case Expected Output
        try:
            expected_result.append(split_test_case[3])
        except Exception:
            expected_result.append('error')

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

