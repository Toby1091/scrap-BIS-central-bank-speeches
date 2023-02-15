# This script outputs the total number of speeches by central bank
import json
import pprint

# from config import RESULT_FILE

with open('output/speech_metadata.json') as file_handle:
    speech_metadata = json.loads(file_handle.read())

uncounted_cb_list = []
cb_count_dict = {'Missing': 0}

for dict in speech_metadata:
    if 'bank_name' in dict or  dict['bank_name'] is None:
        central_bank_name = dict['bank_name']

        if central_bank_name in cb_count_dict:
            cb_count_dict[central_bank_name] += 1
        else:
            cb_count_dict[central_bank_name] = 1
    else:
        cb_count_dict['Missing'] += 1

pprint.pprint(cb_count_dict)

with open('output/keyword_by_speech_all.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        headers = ['bank', 'speech count']
        headers.extend(keywords)
        writer.writerow(headers)


