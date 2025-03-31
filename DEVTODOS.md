# Next Gen QA
- Dev TODOS

# Setup Commit Notes (01-09-2025)
- created folders
- TODO : 
  - [x] fill up components with prototype code
    - start development procedure
  - [x] fill up fine-tuning with prototype code
    - start information processing procedure
  - [x] start django folder setup: django-admin startproject nextgen next-gen-qa (the names felt a bit ambiguous so it is changed to ngq_project from the folder name of django_ngq)

# TODOS (01-13-2025) (backend) (Updated: 01-14-2025)
- [x] development of scraper, prompt generator, and table generator (python) using prototype (V1)
  - [x] development of dataset generator (fine-tuning) using prototype (V1)

# Next TODOS (01-18-2025) (backend) (Updated: 01-28-2025)
- [x] finishing setups of ngq_project, ngq_app, for easy component integration (django)
  - [x] basic connections
  - [x] saving form data and showing results
    - Current Plan:
      - 1. Get Form Data from home.html (suggestion: change to index.html)
      - 2. Go to loading.html and process form data there
      - 3. Load results.html once form data is processed and transferred
- [x] development (scraper, prompt generator, llm, table generator, backend) for system proper
      - [x] Adjust/Recode for system proper
    - Table Generator
      - [x] Code for developing the test case tables
    - Dataset Generator
      - Add Loop and List Methods for easier scraping and generation for a list of URLs

# Extra TODOS (Updated: 01-28-2025)
- [-] Hugging Face Implementation Version of using Llama 3.1 8b

# Next TODOS (01-31-2025) (backend) (Updated: 02-14-2025)
- [x] Cycle 2 Development
    - TODO Compilation:
      - Scraper
        - [x] Add Driver Checking (Checking what browser to use for scraping purposes)
        - [x] Polish Scraped Data formatting
      - Prompt Generator
        - [x] Experiment with prompts (datset generation) with peer review
      - Backend-Frontend Connection (Django)
        - [x] script.js
          - adapt current .js file so that all templates can use it
          - the intention is to use django mainly for backend, and using js for things not done in django and for website aesthetic/dyamicness/etc.
      - [x] Fine-Tuning
      - [x] Evaluation Setups

# Next TODOS (02-24-2025) (backend) (Updated: 02-26-2025)
  - [~] Cycle 3 Development
    - [x] Prompt Generator
      - [x] Common Error Fixer / Validator Function
      - [x] Prompt Adjustments
    - [x] Table Generator
      - [x] Invalid Row Checker Function
    - [x] Dataset Generator
      - [x] Adjust Output, Input, Instruction Format
      - [x] Implement Subcomponent Changes
      - [x] Retroactive Adaptation Function (Convert old dataset to proper format)
    - [x] LLM Fine-Tuning (Cycle 2 Remnant Experiments)
      - [x] Adjustments/Improvements from previous cycle
        - Only save LORA
        - Trial and Error of Modelfiles and Prompts
          - Input seems to be the CONTEXT, aka the PROMPT CONTEXT. if i use that, then it will actually be appropriate. AAAAAAAAAAAAAAAAAAAAA
          - Use that modelfile template suggestion. it works.
        - [x] Separate Notebooks

# Post-Cycle2 Presentation TODOS (02-26-2025) (backend and frontend) (Updated: 03-14-2025)
  - [x] Cycle 3 Development (Frontend)
    - Home Page Overhauls
      - Separation of FAQ and About
      - Color Design Changes
    - [#Non-Urgent] Javascript file separation
    - [x] Results Page Overhaulsg
    - [x] Print/Download Button
        - convert csv->html->pdf
  - [~] Cycle 4 Development (Backend)
    - [#Non-Urgent-Difficult#Planning] Experimentation : Dynamic Results Page
      - Revamps Required:
        - Scraper : Creates a List of Lists of Batches, of 5 ideally. Outputs List of List of Elements, and List of List of subids.
        - [ ] **Prompt Generator+LLM** : Asynchronous - For Each Batch, Output a Batch of LLM Outputs
        - Table Generator : Asynchronous (After Prompt Generator) - For Each Batch, update an existing table
          - Update Existing table:
            - Append All Elements
            - Categorize According to Type
        - Django Backend:
          - Results Page with Loading Elements
            - run main process loop, for each batch done, emit {batch-done} signal, if all batches done, emit {finished} signal
            - for each {batch-done} run results-loading page render {PROBLEM: This reloads the init run script}
            - if {finished}, no more reloading of results.
    - [#In-Progress] Deployment 
      - [x] Django : Security Setup / Keys
        - Remember to securely setup secret key when deploying to server
      - [#] Git Clone To Server
    - [x] Evaluation Tests
      - [x] Multiple Tests and Outputs
        - [x] List of lists of Test Parameters
        - [x] For Loop Iteration
          - [x] Train -> set parameters
          - [x] Test -> get perplexity
          - [x] Clean numbers for formatting (remove decimal places)
          - [x] Download -> set folder filename to f"{train_parameters}-{training_loss}-{perplexity} model"
      - [x] SelfcheckGPT
        - [x] Data prep fixing
        - [x] Use different LLM?
        - Decide whether to redelegate this to Human Evaluation
        - Can TRY to integrate, but we'll see in cycle 3
      - [#] Human Evaluation

# RE: Cycle 3 Todos (Updated: 03-25-2025)
## Section 1: Cleanup + Adding Credits
- [x] Cleanup + Etc. (Documentation, Basic Security Measure, Etc.)
  - [x] Prompt Generator + LLM
  - [x] Scraper
  - [x] Table Generator
  - [x] Dataset Generator
  - [x] Dataset Correction
  - [x] Fine Tuning Evaluation
    - [x] Evaluation
    - [x] Fine Tuning
  - [x] Django App
    - [x] Utils
    - [x] Urls
    - [x] Settings
    - [x] Views
      - Further cleaning after decisions are 
    - [x] Static : Javascript
    - [x] Static : CSS
    - [x] Templates : HTML Pages
    - [x] TemplateTags : Index Filter
- [x] Adding Credits
  - [x] Prompt Generator + LLM
  - [x] Scraper
  - [x] Table Generator
  - [x] Dataset Generator
  - [x] Dataset Correction
  - [x] Fine Tuning Evaluation
    - [x] Evaluation
    - [x] Fine Tuning
  - [x] Django App
    - [x] Utils
    - [x] Static : Javascript
    - [x] Static : CSS
    - [x] Templates : HTML Pages
    - [x] TemplateTags : Index Filter
- [-] Make Repository Public

## Section 2: Finetuning Model
- [x] The Final Run of CYCLE 3 FINETUNING EVALUATION
  - [x] Cycle 1 - 1000
    - [x] 1st Parameter Set (Training Loss: 0.008100 | Perplexity: 3.006251573562622)
      - Does not infinitely generate when temperature == 0
      - Format is not like the dataset, but close enough.
        - Only 1 sentence precondition
        - Sometimes 1 sentence expected result
    - [x] 2nd Parameter Set (Training Loss: 0.008400 | Perplexity: Perplexity: 3.1807754039764404)
      - Seems there is a risk of infinite generation
      - Format is not like the dataset, but close enough
      - 0.4 temp follows non fine tuned format
  -  ABOVE MODELS DO NOT UNDERGO UNLIMITED GENERATION
  - [x] Cycle 2 - 2000
    - [x] 1st Parameter Set (Training Loss: 0.009500 | Perplexity: 3.095846652984619)
      - Follows format more closely when temperature is not set to anything
    - [x] 2nd Parameter Set (Training Loss: 0.008000 | Perplexity: 3.296351909637451)
  - [x] Cycle 3 - 3000
    - [x] 1st Parameter Set (Training Loss: 0.007800 | Perplexity: 3.3332083225250244)
    - [x] 2nd Parameter Set (Training Loss: 0.008300 | Perplexity: 3.569732666015625)
      - Modelfile Drastically changes output of resulting model
  - [x] Final Cycle - Max
    - [x] 1st Parameter Set (Training Loss: 0.008800 | Perplexity: 3.2280256748199463)
    - [-FailedToSave] 2nd Parameter Set (Training Loss: 0.008900 | Perplexity: 3.518860101699829)
- [-] Optional : Empty Input Dataset Models
- [~] Additional : Optimization
  - [x] Train Models
    - [x] Something's Off
      - 2_4_5_10_0.0002_3.1264_lora_model Training Loss 0.013600 
      - 2_8_5_15_0.0001_3.1859_lora_model Training Loss 0.014200
      - 2_4_5_15_0.0002_7.0222_lora_model Training Loss 0.016700
      - 2_8_5_20_0.0001_6.5799_lora_model Training Loss 0.018900
    - [-] Testing Old Format
      - <>   Training Loss 
      - <>   Training Loss 
      - <>   Training Loss 
      - <>   Training Loss 
  - [-] Download Models
  - [-] Test Model

## Section 2.A Fine Tuning Model [Fixed]
- [x] Finetuning properly
- [x] Downloading Models
- [x] Testing
    - <applied-to-rest> requires extra stop parameters
  - [x] 1000 with input
    - [x] 30 epochs 1e-4 learning rate : does not follow test steps format
    - [x] 20 epochs 2e-4 learning rate : does not follow test steps format 
  - [x] 1000 without input
    - [x] 30 epochs 1e-4 learning rate : does not follow format
    - [x] 20 epochs 2e-4 learning rate : fails to place tilde, but follows format
  - [x] 2000 with input
    - [x] 30 1e-4 : does not follow format well 
    - [x] abberant batch sizes, 20 2e-4 : overfitted, infinitely generates 
  - [x] 2000 without input
    - [x] 30 1e-4 : fails to follow format
    - [x] 20 2e-4 : fails to place tilde, can use \n\n as separator instead
  - [x] 3000 with input
    - [x] 30 1e-4 : fails to follow test step format
    - [x] 20 2e-4 : fails to follow test step format
  - [x] 3000 without input
    - [x] 30 1e-4 : does not follow format
    - [x] 20 2e-4 : follows format perfectly 
  - [x] Max with input
    - [x] 30 1e-4 : does not follow test step format properly
    - [x] 20 2e-4 : does not follow test step format properly
  - [x] Max without input
    - [x] 30 1e-4 : does not follow format
    - [x] 20 1e-4 : follows format perfectly
- [x] Practical Testing : Dataset Generator
- [x] Conclusion
  - Used 30 Epochs, 2e-4 Model with Detailed Modelfile Instructions

## Section 3.A [Requires Section 1 to be completed]: Deployment
- [-] Git Pull
- [-] Basic Security Setup
- [-] Run Server

## Section 3.B [Requires Section 1 to be completed]: Dynamic Results Page
- [-] Planning / Discussion
  - Prompt Generator+LLM : Asynchronous - For Each Batch, Output a Batch of LLM Outputs
  - Table Generator : Asynchronous (After Prompt Generator) - For Each Batch, update an existing table
    - Update Existing table:
      - Append All Elements
      - Categorize According to Type
  - Django Backend:
    - Results Page with Loading Elements
      - run main process loop, for each batch done, emit {batch-done} signal, if all batches done, emit {finished} signal
      - for each {batch-done} run results-loading page render {PROBLEM: This reloads the init run script}
      - if {finished}, no more reloading of results.
- [x] **PLAN A Branch : Little to No Dependencies**
  - Integrate render to the prompt generator loop
  - Every after a test case is generated, render the page / update the page with AJAX
  - [x] Reimplementation
  - [X] Implement Frontend
  - [ ] Polishing
    - Ensure connection establishment and closing
    - Major Issue : Multi Tab Running - Websocket Connection
- [#] PLAN B Branch : All The Dependencies
  - Use Celery and its dependencies to make an asynchronous function

# Optional TODOS (Updated: 03-14-2025)
  - Prompt Generator + LLM : add time to generation to check time generated per test case

# RE: Cycle 3 Todos (Updated: 03-31-2025)
## Section 1
- [x] UI Final Implementation
- [ ] Final Polishing + Creditatio-
- [ ] Make Repository Public

## Section 2 [Requires Section 1 to be completed]: Deployment
- [ ] Git Pull
- [ ] Basic Security Setup
- [ ] Run Server