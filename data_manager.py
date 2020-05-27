from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import sql_connection

@sql_connection.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC;"""
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
