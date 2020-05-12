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


get_data(FILENAME, PATH):

    with open(PATH + FILENAME, 'r') as f:
        data = csv.reader(f)
        list_of_rows = list(data)
        list_of_rows.reverse()
    return list_of_rows

save_data(ANS_FILENAME, QUE_FILENAME)

def get_all_user_story(PATH,FILENAME, data):
    data.reverse()
    with open(PATH+FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

