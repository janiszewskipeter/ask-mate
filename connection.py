
import csv

ANS_FILENAME = 'answer.csv'
QUE_FILENAME = 'question.csv'


def get_data(FILENAME, PATH):
 with open(PATH +'/sample_data/'+FILENAME, 'r') as f:
     data = csv.reader(f)
     list_of_rows = list(data)
 return list_of_rows


def save_data(PATH,FILENAME, data, mode):
 with open(PATH +'/sample_data/'+ FILENAME, mode, newline='') as f:
     writer = csv.writer(f)
     writer.writerow(data)

def save_edited_data(PATH,FILENAME, data, mode):
 with open(PATH +'/sample_data/'+ FILENAME, mode, newline='') as f:
     for row in data:
         writer = csv.writer(f)
         writer.writerow(row)


