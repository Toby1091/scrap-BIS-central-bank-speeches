"""
The script analyzes all files in this directory (i.e. a large data set of txt files of central bankers speeches) 
(url: https://www.bis.org/cbspeeches/index.htm). It counts the mentions of each keyword for each file.
"""


# TODO: 
# - make script insensitive to accents (using regular expressions), lower case etc.
# - allow for small variation in order of words (e.g. labor market equilibrium vs. equilibrium in labor markets)
# - Lemmatization/stemming: https://towardsai.net/p/data-mining/text-mining-in-python-steps-and-examples-78b3f8fd913b#:~:text=than%20Porter%20stemmer.-,Lemmatization,-In%20simpler%20terms
# - implement a switch to count only keywords where count > 10

import os
import json

import helpers

KEYWORDS = helpers.read_keywords_file()

with open('output/speech_metadata.json') as file_handle:
    speech_metadata = json.loads(file_handle.read())

keyword_count_by_speech = {}

for speech_info in speech_metadata:
    if not speech_info['pdf_path']:
        continue
    txt_file_name = speech_info['pdf_path'].split('/')[2].replace('.pdf', '.txt')
    joined_file_path = os.path.join('output/textified_pdfs', txt_file_name) # function adds a / between the two arguments
    with open(joined_file_path) as file_handle: # this is where we actually open the file
        
        content = file_handle.read().lower().replace('\n', ' ')

    keywords = {}

    for keyword in KEYWORDS:
        count = content.count(keyword)
        if count > 0:
            keywords[keyword] = count

    keyword_count_by_speech[txt_file_name] = keywords

with open('output/keyword_by_speech_output.json', 'w') as f:
    json.dump(keyword_count_by_speech, f, indent=4)
