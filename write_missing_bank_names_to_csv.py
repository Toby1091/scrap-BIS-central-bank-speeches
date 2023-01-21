# This script outputs a csv (of the subheadings) of all speeches where the bank_name is missing
import json
import pprint
import csv

from config import RESULT_FILE

with open(RESULT_FILE) as file_handle:
    speech_metadata = json.loads(file_handle.read())


csv_of_metadata_by_cb = open('speeches_by_cb.csv', 'w')

headers = ["pdf_path", "subheading"] 

writer = csv.writer(csv_of_metadata_by_cb)
writer.writerow(headers)

for dict in speech_metadata:
    if not dict.get('bank_name'):
        row = []
        for header in headers:
            row.append(dict.get(header, ''))
        writer.writerow(row)

        pprint.pprint(dict)
        
csv_of_metadata_by_cb.close()
