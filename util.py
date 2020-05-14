from flask import Flask, render_template, request, redirect, url_for
import time
import string
import random

'''
Helper functions which can be called from any other layer.
(but mainly from the business logic layer)
'''

def id_generator():
    id = []
    for i in range(5):
        letter = random.choice(string.ascii_letters)
        id.append(letter)
    id = ''.join(id)

    return id

def get_time():
    named_tuple = time.localtime()
    current_time= time.strftime("%H:%M", named_tuple)
    return current_time

def sort():
    questions = connection.get_data('question.csv', PATH)
    TIME_INDEX = 1
    sorted_question = sorted(questions, key=lambda questions: questions[TIME_INDEX])
    pass

    return sorted_question
def add_headers():
    pass