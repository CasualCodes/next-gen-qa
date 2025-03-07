# Next Gen QA
- Repository for the thesis project "Next-Gen Website QA: Automated Functional Test Case Creation Using Large Language Models, Prompt Engineering, and Scraping Technologies"

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

# Post-Cycle2 Presentation TODOS (02-26-2025) (backend and frontend) (Updated: 03-07-2025)
  - [x] Cycle 3 Development (Frontend)
    - Home Page Overhauls
      - Separation of FAQ and About
      - Color Design Changes
    - [#Non-Urgent] Javascript file separation
    - [x] Results Page Overhauls
    - Besides **displaying** number of test cases, display number of test cases per element
      Plan IV:
        [x] Planning
        [x] Design
        [x] Coding
        [x] Testing
    - [x] Print/Download Button
        - convert csv->html->pdf
  - [ ] Cycle 4 Development (Backend)
    - [#Non-Urgent-Difficult] Experimentation : Dynamic Results Page
    - [#In-Progress] Deployment 
      - [x] Django : Security Setup / Keys
        - Remember to securely setup secret key when deploying to server
      - [#] Git Clone To Server
    - [ ] Evaluation Tests
      - [ ] SelfcheckGPT
        - [ ] Data prep fixing
        - [ ] Use different LLM?
        - Decide whether to redelegate this to Human Evaluation
      - [ ] Human Evaluation
  