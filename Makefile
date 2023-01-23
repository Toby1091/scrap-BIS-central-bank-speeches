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
	python -m unittest discover -p "*_test.py"