# This script outputs the total number of speeches by central bank
import json
import pprint

from config import RESULT_FILE

with open(RESULT_FILE) as file_handle:
    speech_metadata = json.loads(file_handle.read())

uncounted_cb_list = []
cb_count_dict = {'Missing': 0}

for dict in speech_metadata:
    if 'central_bank' in dict:
        central_bank_name = dict['central_bank']

        if central_bank_name in cb_count_dict:
            cb_count_dict[central_bank_name] += 1
        else:
            cb_count_dict[central_bank_name] = 1
    else:
        cb_count_dict['Missing'] += 1

pprint.pprint(cb_count_dict)

# Create a list of dictionaries. Each central bank gets one dictionary. Key-value pairs are: cb name, total number of speeches, 
# and then for each keyword a key-value pair
# it should look like this name_of_cb = [{'total_number_speeches: ': cb_count_dict}, {keyword1: count}, {keyword2: count}]
