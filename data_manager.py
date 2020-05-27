from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import sql_connection

'''
Layer between the server and the data.
Functions here should be called from the server.py
and these should use generic functions from the connection.py
'''

@connection.connection_handler
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
        SELECT id, submission_time, question_id, vote_number, message, image
        FROM answer
        WHERE id = (%s)
        ORDER BY submission_time""", [id])
    return cursor.fetchall()

@sql_connection.connection_handler
def get_comment_by_id(cursor: RealDictCursor, id: int) -> list:
    cursor.execute("""
        SELECT id, question_id,  submission_time, message, image
        FROM comment
        WHERE id = (%s)
        ORDER BY submission_time""", [id])
    return cursor.fetchall()


@sql_connection.connection_handler
def add_commnet_to_qustion(cursor: RealDictCursor, question_id: int, answer_id: int, message: str, submission_time: str, edited_count: int ) -> list:
@sql_connection.connection_handler
def add_commnet_to_qustion(cursor: RealDictCursor, question_id: int, answer_id: int, message_text: str, submission_time: str, edited_count: int ) -> list:
    cursor.execute("""
        INSERT INTO commnet 
        VALUES ((%s),(%s),(%s), TIMESTAMP WITHOUT TIME ZONE, (%s))
        ORDER BY submission_time""", [question_id, answer_id, message_text, submission_time, edited_count])
    return cursor.fetchall()


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
def new_question(cursor: RealDictCursor, id: int) -> list:
    cursor.execute("""INSERT INTO question
    VALUES (%(id)s,%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s);""",
                   new_question)

@sql_connection.connection_handler
def read_a_question(cursor: RealDictCursor, id: int) -> list:
    cursor.execute("""
                    SELECT * FROM question
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
