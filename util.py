import time

'''
Helper functions which can be called from any other layer.
(but mainly from the business logic layer)
'''

def id_generator():
    pass
def get_time():
    named_tuple = time.localtime()
    current_time= time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)


    return current_time
def sort():
    pass
def add_headers():
    pass