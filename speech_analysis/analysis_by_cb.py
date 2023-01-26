import json
import pprint

with open ('output/speech_metadata.json', 'r') as file_handle:
    speech_metadata = json.loads(file_handle.read())

cb_list = {}

with open('output/keyword_by_speech_output.json', 'r') as file_handle:
    keywords_by_speech_json = json.loads(file_handle.read())

keyword_dict = {}

    # file_name_from_keywords_by_speech = speech[]
    # new_individual_cb_dict[keyword_from_metadata] = 

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

# TODO: Extract into separate function
for speech_dict in speech_metadata:
    if speech_dict['pdf_path'] is None:
        # Some speeches don't have a pdf on the website
        continue

    # /review/r200924a.pdf --> r200924a
    speech_ID = speech_dict['pdf_path'].replace('/review/', '').replace('.pdf', '')

    cb_name_from_json = speech_dict['bank_name']
    if cb_name_from_json is None:
        # For some speeches we don't know the bank name
        continue

    keywords_source = keywords_by_speech_json.get(speech_ID + '.txt')
    if not keywords_source:
        # TODO: Looks like some speeches don't have a txt file. Why?
        print('Text file missing:', speech_ID + '.txt')
        continue

    keywords_target = cb_list[cb_name_from_json].setdefault('keywords', {})
    for keyword, count in keywords_by_speech_json[speech_ID + '.txt'].items():
        keywords_target.setdefault(keyword, 0)
        keywords_target[keyword] += count

with open('output/keyword_by_bank.json', 'w') as f:
    json.dump(cb_list, f, indent=4)



# for each speech_dict in speech_metadata, find corresponding dict in keyword_by_speech_output and add this dict 
# as a new item to the innerdict of cb_list, that is, a new item of new_individual_cb_dict
# once it has been added, the second time around, only increase the count of the given keywords




pprint.pprint(cb_list)

# for cb_name_from_json in cb_list:
#     if cb_list[cb_name_from_json]['total_count_speeches'] > 10:
#         print(cb_name_from_json + ':', cb_list[cb_name_from_json]['total_count_speeches'])



# cb_list = [
# {
#     'cb_name': 'Bank of Canada', 
#     'total_count_speeches': 50, 
#     'keywords': {
#         'natural': 3,
#         'neutral' 1
#     }
#   }, 
# {
#     'cb_name': 'Bank of Greece', 
#     'total_count_speeches': 50, 
#     'keywords': 'dict_of_keywords'
#   }
# ]

