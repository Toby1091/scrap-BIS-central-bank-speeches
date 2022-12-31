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


