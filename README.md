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

# Next TODOS (01-18-2025) (backend) (Updated: 01-18-2025)
- [ ] development (scraper, prompt generator, llm, table generator, backend) for system proper
  - TODO Compilation:
    - Scraper
      - Add Driver Checking (Checking what browser to use for scraping purposes)
    - Prompt Generator
      - Experiment with prompts (datset generation)
      - Adjust/Recode for system proper
    - Table Generator
      - Code for developing the test case tables
    - Dataset Generator
      - Add Loop and List Methods for easier scraping and generation for a list of URLs
- [ ] finishing setups of ngq_project, ngq_app, for easy component integration (django)