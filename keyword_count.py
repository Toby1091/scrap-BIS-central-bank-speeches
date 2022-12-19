"""
The script analyzes all files in this directory (i.e. a large data set of txt files of central bankers speeches) 
(url: https://www.bis.org/cbspeeches/index.htm). It computes a total count of each keyword of a list of keywords across all files.
"""


# TODO: 
# - make script insensitive to accents (using regular expressions), lower case etc.
# - allow for small variation in order of words (e.g. labor market equilibrium vs. equilibrium in labor markets)
# Lemmatization/stemming: https://towardsai.net/p/data-mining/text-mining-in-python-steps-and-examples-78b3f8fd913b#:~:text=than%20Porter%20stemmer.-,Lemmatization,-In%20simpler%20terms
import os

with open("list_of_keywords.txt") as file_handle:
    content = file_handle.read()

KEYWORDS = content.split('\n')

speech_directory = 'txt'

txt_file_names = os.listdir(speech_directory)

keyword_count = {}

for keyword in KEYWORDS: # Creates a new variable (in this case called "keyword") for every element of the list KEYWORDS...
    keyword_count[keyword] = 0 #...runs the following code, after loop is run, the variable is deleted from memory & the next list element is taken as a variable)

for txt_file_name in txt_file_names: 
    joined_file_path = os.path.join(speech_directory, txt_file_name) # function adds a / between the two arguments
    with open(joined_file_path) as file_handle: # this is where we actually open the file

        content = file_handle.read().lower()

    for keyword in KEYWORDS:
        keyword_count[keyword] = keyword_count[keyword] + content.count(keyword)

for keyword in keyword_count:
    print(keyword, ":", keyword_count[keyword])

total_count = 0

for keyword in keyword_count:
    total_count += keyword_count[keyword] #This is a shortcut total_count = total_count + keyword_count_dict[dict_entry]

print('Total count: ', total_count)
