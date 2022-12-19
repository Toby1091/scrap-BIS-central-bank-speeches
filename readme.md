
Current working directory: pwd
- git clone git@github.com:Toby1091/scrap-BIS-central-bank-speeches.git
- python -m venv .venv (creates virtual environment)
- source .venv/bin/activate
- python -m pip install -r requirements.txt
- scrapy runspider scrap_speeches.py -o speeches.jsonl 



3 Steps:

1. Scrape data
Download HTML and PDF files from https://www.bis.org

2. Prepare data
Convert PDF to text
Clean text
Prepare meta data

3. Analyse data
Search text