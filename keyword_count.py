"""

Explain here the goal of the script, 
Script analyzes all files in this directory and for the list of the keywords it counts the number of mentions

"""

import os

KEYWORDS = ['natural rate', 'natural level', 'natural rate of unemployment', 'natural unemployment rate', 'u*', 'NAIRU', 
'natural rate of interest', 'natural interest rate', 'r*', 'potential output', 'potential growth', 'Y*', 'trend growth', 
'long-term rate of', 'neutral rate of interest', 'neutral interest rate', 'neutral real interest rate ', 
'short-term real interest rate', 'equilibrium rate', 'output gap']

speech_txt_path = 'txt/'

txt_file_names = os.listdir(speech_txt_path)

keyword_count = {}

for keyword in KEYWORDS: #creates a new variable (in this case called "keyword") for every element of the list KEYWORDS...
    keyword_count[keyword] = 0 #...runs the following code, after loop is run, the variable is deleted from memory & the next list element is taken as a variable)

for txt_file_name in txt_file_names: 
    f = open(speech_txt_path + txt_file_name)

    content = f.read()

    for keyword in KEYWORDS:
        keyword_count[keyword] = keyword_count[keyword] + content.count(keyword)

for keyword in keyword_count:
    print(keyword, ":", keyword_count[keyword])

total_count = 0

for keyword in keyword_count:
    total_count += keyword_count[keyword] #this is a shortcut total_count = total_count + keyword_count_dict[dict_entry]

print('Total count: ', total_count)
