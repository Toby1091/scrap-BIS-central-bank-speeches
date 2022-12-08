"""
The script analyzes all files in this directory (i.e. a large data set of txt files of central bankers speeches) 
(url: https://www.bis.org/cbspeeches/index.htm). It computes a total count of each keyword of a list of keywords across all files.
"""


# TODO: 

import os

KEYWORDS = ['natural rate', 'natural level', 'natural rate of unemployment', 'natural unemployment rate', 'u*', 'N*', 'nairu', 'NIRU', 'nawru',
'non-accelerating inflation rate of unemployment', 'noncyclical rate of unemployment', 'natural rate of interest', 'natural interest rate', 'r*', 'potential output', 
'potential growth', 'Y*', 'trend growth', 'long-term rate of', 'long-run rate of', 'neutral rate of interest', 'neutral interest rate', 
'neutral real interest rate ', 'short-term real interest rate', 'equilibrium rate', 'output gap']
'non-accelerating inflation rate of unemployment', 'noncyclical rate of unemployment', 'natural rate of interest', 'natural interest rate', 
'neutral interest rate', 'neutral real interest rate ', 'equilibrium real rate of interest', 'equilibrium rate', 
'short-term real interest rate', 'output gap']

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
