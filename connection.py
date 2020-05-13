'''
Common functions to read/write/append CSV files without
feature specific knowledge.
The layer that have access to any kind of
long term data storage. In this case, we use CSV files,
but later on we'll change this to SQL database.

'''

import csv

# ANS_FILENAME = answer.csv
# QUE_FILENAME = question.csv


def get_data(FILENAME, PATH):
    with open(PATH +'/sample_data/'+FILENAME, 'r') as f:
        data = csv.reader(f)
        list_of_rows = list(data)
    return list_of_rows



def save_data(PATH,FILENAME, data):
    with open(PATH +'/sample_data/'+ FILENAME, 'w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)




