# Plug in your logic code here (Scraper, Prompt Generator, Fine Tuned LLM, And Table Generator)
# TODO : Code Integration and utils.py connection

## Scraper
# VERSION 1 [PORTED FROM COMPONENTS FOLDER]
## SCRAPER IMPORTS ##
from selenium import webdriver

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

## GET URL FUNCTION (non UI version) ##
def get_url():
    return input("Enter Website URL: ")

# DATA SCRAPING FUNCTION
def data_scrape(url):
    # Setup Selenium Webdriver
    # TODO : For V2 Add other drivers according to user settings. Detect user browser and use that as driver potentially
    driver = webdriver.Firefox()
    # Setup Return Data
    data = []

    # Open the website
    driver.get(url)
    
    ## GET UI ELEMENTS (must be visible) ##

    # BUTTONS
    buttons = driver.find_elements(By.CSS_SELECTOR, "button")
    for button in buttons:
        if button.is_displayed():
            # Button Element Attributes
            button_text = f"Button Element '{button.text}'" if (button.text != None and button.text != "") else "Button Element Without Name"
            button_size = f"With Size Attribute {button.size}" if button.size != None else "Without Size Attribute"
            button_color = f"With Background Color {button.value_of_css_property("background-color")}" if button.value_of_css_property("background-color") != None else "Without Background Color"
            button_enabled = "and the button is Clickable" if button.is_enabled() else "and the button is not Clickable"
            
            # Store Button Element
            store = f"{button_text} {button_size} {button_color} {button_enabled}"
            data.append(store)
            
    # LINKS
    links = driver.find_elements(By.TAG_NAME,"a")
    for link in links:
        if link.is_displayed():
            # Link Element Attributes
            link_text = f"Link Element '{link.text}'" if (link.text != None and link.text != "") else "Link Element Without Name"
            link_url = f"With URL {link.get_attribute('href')}" if link.get_attribute('href') != None else "Without URL"
            # Additional Attributes
            link_rel = f"With rel attribute {link.get_attribute('rel')}" if link.get_attribute('rel') != None and link.get_attribute('rel') != "" else ""
            link_target = f"With target attribute {link.get_attribute('target')}" if link.get_attribute('target') != None and link.get_attribute('target') != "" else ""
            link_download = f"This is a download link to document {link.get_attribute('download')}" if link.get_attribute('download') != None and link.get_attribute('download') != "" else ""
            
            # Store Link Element
            store = f"{link_text} {link_url} {link_rel} {link_target} {link_download}"
            data.append(store)

    # VISIBLE TEXT
    # Heading Elements
    for level in range(1, 7):  # HTML has 6 levels of headings (h1 to h6)
        headings = driver.find_elements(By.TAG_NAME,f"h{level}")
        for heading in headings:
            if heading.is_displayed():
                store = f"Heading Element (h{level}): '{heading.text}'"
                # Store
                data.append(store)
    # Paragraph Elements
    paragraphs = driver.find_elements(By.TAG_NAME,"p")
    for paragraph in paragraphs:
        if paragraph.is_displayed():
            store = f"Paragraph Element: '{paragraph.text}'"
            # Store
            data.append(store)

    # INPUT
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
            input_field_disabled = f"Is Not Clickable" if input_tag.get_attribute('disabled') != None else "Is Clickable"
            input_field_required = f"Is Required" if input_tag.get_attribute('required') != None else "Not Required"
            input_field_autocomplete = f"Is Autocomplete" if input_tag.get_attribute('autocomplete') != None else "Not Autocomplete"

            # Store based on type
            if (input_tag.get_attribute('type') == "submit"):
                store = f"Form Submit Button Element: {input_tag.get_attribute("name")} {input_field_disabled}"
            else:
                store = f"{input_field_name} {input_field_type} {input_field_required} {input_field_value} {input_field_placeholder} {input_field_readonly} {input_field_disabled} {input_field_autocomplete}"
            data.append(store)
            
    # Close the browser
    driver.quit()
    
    ## RETURN COMPILED ELEMENT DATA ##
    return data

## Prompt Generator + LLM
# VERSION 1 [PORTED FROM COMPONENTS FOLDER]

# Langchain and Ollama
import langchain
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# CONTEXT V1
template = """ Question:\n Generate test case for the following UI element: : {question} """
model_str = "llama3.1"

# Prompt Generator + LLM
# Load Model Chain
def load_model_chain(template : str =  template, model_str : str = model_str):
    # TODO : Plug In Fine Tuned Model
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model=model_str)
    chain = prompt | model
    return chain

# Create Test Case Data
def create_test_cases(data):
    
    # Load LLM Chain
    chain = load_model_chain()

    # Return Data
    return_data = []
    
    for item in data:
        return_data.append(chain.invoke({"question": str(item)}))
        # LLM Reset To Free Up Context
        chain = load_model_chain()

    return return_data

## Table Generator
# VERSION 1 [PORTED FROM COMPONENTS FOLDER]

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
    # TODO : After Dataset Generator Development

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

