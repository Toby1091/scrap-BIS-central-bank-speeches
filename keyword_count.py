import os

keywords = ['natural rate', 'natural level', 'natural rate of unemployment', 'natural unemployment rate', 'u*', 'NAIRU', 
'natural rate of interest', 'natural interest rate', 'r*', 'potential output', 'potential growth', 'Y*', 'trend growth', 
'long-term rate of', 'neutral rate of interest', 'neutral interest rate', 'neutral real interest rate ', 
'short-term real interest rate', 'equilibrium rate', 'output gap']

txt_files = os.listdir('txt/')

keyword_count_dict = {} # initialize count with 0 

for keyword in keywords:
    keyword_count_dict[keyword] = 0

#creates a new variable (in this case called "txt_file") for every element of the list txt_files
#and runs the following code, after the loop is run, the variable is deleted from memory and the next list element is taken as a variable)

for txt_file in txt_files: 
    #print('\n', txt_file)
    f = open('txt/' + txt_file)

    print(txt_file)

    content = f.read()

    for keyword in keywords:
        #print(keyword + ": ", content.count(keyword))
        #keyword_count = keyword_count + content.count(keyword)
        keyword_count_dict[keyword] = keyword_count_dict[keyword] + content.count(keyword)

#print("\nTotal: ", keyword_count,'\n')

for dict_entry in keyword_count_dict:
    print(dict_entry, ":", keyword_count_dict[dict_entry])

#To compute Total from the dictionary
total_count = 0 

for dict_entry in keyword_count_dict:
    total_count += keyword_count_dict[dict_entry] #this is a shortcut total_count = total_count + keyword_count_dict[dict_entry]


print('Total count: ', total_count)
