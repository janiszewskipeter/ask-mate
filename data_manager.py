from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import time

import sql_connection

'''
Layer between the server and the data.
Functions here should be called from the server.py
and these should use generic functions from the connection.py
'''

@sql_connection.connection_handler
def get_question_by_id(cursor: RealDictCursor, id: int) -> list:
    cursor.execute("""
        SELECT id, submission_time, view_number, vote_number, title, message, image
        FROM question
        WHERE id = (%s)
        ORDER BY submission_time""", [id])
    return cursor.fetchall()


@sql_connection.connection_handler
def get_answer_by_id(cursor: RealDictCursor, id: int) -> list:
    cursor.execute("""
        SELECT *
        FROM answer
        WHERE id = (%s)
        ORDER BY submission_time""", [id])
    return cursor.fetchall()


@sql_connection.connection_handler
def get_comment_by_id(cursor: RealDictCursor, id: int) -> list:
    cursor.execute("""
        SELECT *
        FROM comment
        WHERE question_id = (%s)
        ORDER BY submission_time""", [id])
    return cursor.fetchall()


def add_commnet_to_qustion(cursor: RealDictCursor, question_id: int, message: str, edited_count: int ) -> list:
    cursor.execute("""
        INSERT INTO comment(question_id, message, submission_time, edited_count)
        VALUES ((%s),(%s), CURRENT_TIMESTAMP, (%s))
        """, [question_id, message, edited_count])


@sql_connection.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time;"""
    cursor.execute(query)
    return cursor.fetchall()

@sql_connection.connection_handler
def get_answers(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM answer
        ORDER BY submission_time;"""
    cursor.execute(query)
    return cursor.fetchall()


@sql_connection.connection_handler
def get_first_five_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT * 
        FROM question 
        ORDER BY submission_time DESC
        LIMIT 5;"""
    cursor.execute(query)
    return cursor.fetchall()

@sql_connection.connection_handler
def add_question(cursor: RealDictCursor, title: str, message: str) -> list:
    cursor.execute("""INSERT INTO question(submission_time, title, message)
                        VALUES (CURRENT_TIMESTAMP, (%s), (%s));
                        """, [title, message])


@sql_connection.connection_handler
def read_a_question(cursor: RealDictCursor, id: int) -> list:
    cursor.execute("""SELECT * FROM question
                WHERE id=%(id)s;
                """,
               {'id': id})
    questions = cursor.fetchall()
    return questions


@sql_connection.connection_handler
def answer_by_question_id(cursor: RealDictCursor, id: int) -> list:
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id=%(id)s;
                    """,
                   {'id': id})
    answers = cursor.fetchall()
    return answers

def get_new_question_id():
    questions = get_questions()
    max_id = "0"
    for i in questions:
        if int(max_id) < int(i['id']):
            max_id = i['id']
    max_id = int(max_id) + 1
    return str(max_id)