'''
Common functions to read/write/append CSV files without
feature specific knowledge.
The layer that have access to any kind of
long term data storage. In this case, we use CSV files,
but later on we'll change this to SQL database.

'''

import os

import psycopg2
import psycopg2.extras


def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper



# import csv
#
# # ANS_FILENAME = answer.csv
# # QUE_FILENAME = question.csv
#
#
# def get_data(FILENAME, PATH):
#     with open(PATH +'/sample_data/'+FILENAME, 'r') as f:
#         data = csv.reader(f)
#         list_of_rows = list(data)
#     return list_of_rows
#
#
# def save_data(PATH,FILENAME, data, mode):
#     with open(PATH +'/sample_data/'+ FILENAME, mode, newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(data)
#
# def save_edited_data(PATH,FILENAME, data, mode):
#     with open(PATH +'/sample_data/'+ FILENAME, mode, newline='') as f:
#         for row in data:
#             writer = csv.writer(f)
#             writer.writerow(row)


