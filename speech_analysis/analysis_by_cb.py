import json
import pprint

with open ('../output/speech_metadata.json', 'r') as file_handle: # with .. go up one folder
    speech_metadata = json.loads(file_handle.read())

cb_list = {}

for speech_dict in speech_metadata:
    cb_name_from_json = speech_dict['bank_name']

    if cb_name_from_json is None: # i.e., if cb_name_form_json has value None, abort current iteration & continue for-loop
        continue

    if cb_name_from_json not in cb_list:
        new_individual_cb_dict = {'cb_name': cb_name_from_json, 'total_count_speeches': 1}
        cb_list[cb_name_from_json] = new_individual_cb_dict
        
    else:
        existing_individual_cb_dict = cb_list[cb_name_from_json] # Look for inner dict in cb_list
        existing_individual_cb_dict['total_count_speeches'] += 1 # Increment value in inner dict

with open('keyword_count.py', 'r') as file_handle:
    content = file_handle.read()


# pprint.pprint(cb_list)

for cb_name_from_json in cb_list:
    if cb_list[cb_name_from_json]['total_count_speeches'] > 10:
        print(cb_name_from_json + ':', cb_list[cb_name_from_json]['total_count_speeches'])



# cb_list = [
# {
#     'cb_name': 'Bank of Canada', 
#     'total_count_speeches': 50, 
#     'keywords': 'dict_of_keywords'
#   }, 
# {
#     'cb_name': 'Bank of Greece', 
#     'total_count_speeches': 50, 
#     'keywords': 'dict_of_keywords'
#   }
# ]