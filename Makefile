init:
	pip install -r requirements.txt

# Scrape html files and pdfs; derive missing bank names from HTML
# - Writes: output/www.bis.org, output/speech_metadata.json
scrape:
	python scrape_files.py

# Extend speech_metadata.json with of bank names
# - Reads: output/speech_metadata.json
# - Writes: output/speech_metadata.json
bank_names:
	python bank_names.py output/speech_metadata.json output/speech_metadata.json


# Convert PDFs to text files
# - Reads: output/www.bis.org/review/*.pdf
# - Writes: output/textified_pdfs
convert:
	python convert_pdfs.py

# Search keywords in text files
# - Reads: output/textified_pdfs, speech_analysis/list_of_keywords.txt
# - Writes: output/keyword_by_speech_output.json
count:
	python speech_analysis/keyword_count_by_speech.py

# Aggregates keyword counts by bank
# - Reads: output/speech_metadata.json, output/keyword_by_speech_output.json
# - Writes: output/keyword_by_bank.json
aggregate:
	python speech_analysis/analysis_by_cb.py

# Write aggregated keyword counts to various csv files
# - Reads: output/keyword_by_bank.json, speech_analysis/list_of_keywords.txt
# - Writes: output/keyword_by_speech_all.csv, output/csv_per_bank, output/csv_per_keyword
export_csv:
	python speech_analysis/export_csv.py

test:
	python -m unittest discover -p "*_test.py"