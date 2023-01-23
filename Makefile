init:
	pip install -r requirements.txt
scrape:
	python scrape_files.py
convert:
	python convert_pdfs.py
count:
	python keyword_count.py
analyse:
	python speech_analysis.py
test:
	python bank_names.test.py && python utils.test.py