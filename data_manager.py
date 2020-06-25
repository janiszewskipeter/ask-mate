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
def get_question_by_id(cursor: RealDictCursor, question_id: int) -> list:
    cursor.execute("""
        SELECT *
        FROM question
        WHERE id = (%s)
        ORDER BY submission_time""", [question_id])
    return cursor.fetchall()

@sql_connection.connection_handler
def questions_by_id(cursor: RealDictCursor, user_id: int) -> list:
    query = """
            SELECT id, submission_time, view_number, vote_number, title, message, image
            FROM question
            WHERE id = %(user_id)s
    """
    args = {'user_id': user_id}
    cursor.execute(query, args)
    return cursor.fetchall()

@sql_connection.connection_handler
def get_comment_by_id(cursor: RealDictCursor, comment_id: int) -> list:
    query = """
            SELECT *
            FROM comment
            WHERE id = %(comment_id)s
    """
    args = {'comment_id': comment_id}
    cursor.execute(query, args)
    return cursor.fetchall()

@sql_connection.connection_handler
def get_comments(cursor: RealDictCursor) -> list:
    cursor.execute("""
        SELECT *
        FROM comment
        ORDER BY submission_time""")
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
def get_answer_by_question_id(cursor: RealDictCursor, question_id: int) -> list:
    cursor.execute("""
        SELECT *
        FROM answer
        WHERE id = (%s)
        ORDER BY submission_time""", [question_id])
    return cursor.fetchall()


@sql_connection.connection_handler
def get_comment_by_question_id(cursor: RealDictCursor, question_id: int) -> list:
    cursor.execute("""
        SELECT *
        FROM comment
        WHERE question_id = (%s)
        ORDER BY submission_time""", [question_id])
    return cursor.fetchall()

@sql_connection.connection_handler
def get_comment_by_answer_id(cursor: RealDictCursor, id: int) -> list:
    cursor.execute("""
        SELECT *
        FROM comment
        WHERE answer_id = (%s)
        ORDER BY submission_time""", [id])
    return cursor.fetchall()

@sql_connection.connection_handler
def add_comment_to_qustion(cursor: RealDictCursor, question_id: int, message: str, edited_count: int ) -> list:
    cursor.execute("""
        INSERT INTO comment( question_id, message, submission_time, edited_count)
        VALUES ((%s),(%s), CURRENT_TIMESTAMP, (%s))
        """, [question_id, message, edited_count])

@sql_connection.connection_handler
def add_comment_to_answer(cursor: RealDictCursor, answer_id: int, message: str, edited_count: int) -> list:
    cursor.execute("""
        INSERT INTO comment( answer_id, message, submission_time, edited_count)
        VALUES ((%s),(%s), CURRENT_TIMESTAMP, (%s))
        """, [answer_id, message, edited_count])

@sql_connection.connection_handler
def save_answer(cursor: RealDictCursor, answer: str, question_id: int) -> list:
    cursor.execute("""
        INSERT INTO answer( message, question_id, submission_time)
        VALUES ((%s),(%s), CURRENT_TIMESTAMP)
        """, [answer, question_id])

@sql_connection.connection_handler
def get_question_id_from_answer(cursor: RealDictCursor, answer_id: int) -> list:
    cursor.execute("""
         SELECT question_id
         FROM answer
         WHERE id = (%s)
         """, [answer_id])
    return cursor.fetchone()["question_id"]

@sql_connection.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM question
        ORDER BY submission_time DESC;"""
    cursor.execute(query)
    return cursor.fetchall()

@sql_connection.connection_handler
def get_users(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM users
        ORDER BY registration_time DESC;"""
    cursor.execute(query)
    return cursor.fetchall()

# @sql_connection.connection_handler
# def get_answers(cursor: RealDictCursor) -> list:
#     query = """
#         SELECT *
#         FROM answer
#         ORDER BY submission_time;"""
#     cursor.execute(query)
#     return cursor.fetchall()

@sql_connection.connection_handler
def vote(cursor: RealDictCursor, votes: int, question_id: int) -> list:
    cursor.execute("""
             UPDATE question
             SET vote_number = (%s)
             WHERE id = (%s)
             """, [votes, question_id])

@sql_connection.connection_handler
def vote_answer(cursor: RealDictCursor, votes: int, question_id: int, answer_id: int) -> list:
    cursor.execute("""
             UPDATE answer
             SET vote_number = (%s)
             WHERE question_id = (%s) AND id = (%s)
             """, [votes, question_id, answer_id])

@sql_connection.connection_handler
def search(cursor: RealDictCursor, searched_phrase: str) -> list:
    cursor.execute("""
            SELECT * FROM question       
            WHERE message LIKE (%s) OR title like (%s)
            ORDER BY question.submission_time DESC
             """, ['%'+searched_phrase+'%','%'+searched_phrase+'%'])
    return cursor.fetchall()

@sql_connection.connection_handler
def search_answer(cursor: RealDictCursor, searched_phrase: str) -> list:
    cursor.execute("""
            SELECT * FROM answer
            WHERE message LIKE (%s)
            ORDER BY submission_time DESC
             """, ['%'+searched_phrase+'%'])
    return cursor.fetchall()

@sql_connection.connection_handler
def delete_question(cursor: RealDictCursor, question_id: int) -> list:
    cursor.execute("""
             DELETE FROM question
             WHERE id = (%s)
             """, [question_id])

@sql_connection.connection_handler
def delete_answer(cursor: RealDictCursor,question_id: int, answer_id: int) -> list:
    cursor.execute("""
             DELETE FROM answer
             WHERE question_id = (%s) AND id = (%s)
             """, [question_id, answer_id])

@sql_connection.connection_handler
def delete_question_comment(cursor: RealDictCursor, question_id: int, comment_id: int) -> list:
    cursor.execute("""
             DELETE FROM comment
             WHERE question_id = (%s) AND id = (%s)
             """, [question_id, comment_id])

@sql_connection.connection_handler
def delete_answer_comment(cursor: RealDictCursor, answer_id:int) -> list:
    cursor.execute("""
             DELETE FROM comment
             WHERE answer_id = (%s)
             """, [ answer_id])

@sql_connection.connection_handler
def get_vote_number(cursor: RealDictCursor, question_id: int) -> int:
    cursor.execute("""
             SELECT vote_number
             FROM question
             WHERE id = (%s)
             """, [question_id])
    return cursor.fetchone()['vote_number']

@sql_connection.connection_handler
def get_tags_with_count(cursor: RealDictCursor) -> int:
    cursor.execute("""
             SELECT tag.name AS name, COUNT(tag_id) AS count
             FROM tag
             JOIN question_tag qt on tag.id = qt.tag_id
             GROUP BY tag.name
             """,)
    return cursor.fetchall()

@sql_connection.connection_handler
def get_tags(cursor: RealDictCursor) -> int:
    cursor.execute("""
             SELECT *
             FROM tag
             """,)
    return cursor.fetchall()

@sql_connection.connection_handler
def get_tags_for_question(cursor: RealDictCursor, question_id:int) -> int:
    cursor.execute("""
             SELECT name
             FROM question_tag
             JOIN tag
             ON tag_id = id
             WHERE question_id = (%s)
             """,[question_id])
    return cursor.fetchall()

@sql_connection.connection_handler
def get_tag_id(cursor: RealDictCursor, tag_name: str) -> int:
    cursor.execute("""
             SELECT tag_id
             FROM question_tag
             JOIN tag
             ON tag_id = id
             WHERE name = (%s)
             """,[tag_name])
    return cursor.fetchone()['tag_id']

@sql_connection.connection_handler
def add_tag_to_question(cursor: RealDictCursor, question_id, tag_id) -> int:
    cursor.execute("""
             INSERT INTO question_tag(question_id, tag_id )
             VALUES ((%s),(%s))
             """,[question_id, tag_id])

@sql_connection.connection_handler
def delete_tag_from_question(cursor: RealDictCursor, question_id, tag_id) -> int:
    cursor.execute("""
             DELETE FROM question_tag
             WHERE question_id = (%s) AND tag_id = (%s)
             """,[question_id, tag_id])

@sql_connection.connection_handler
def add_new_tag(cursor: RealDictCursor, new_tag) -> int:
    cursor.execute("""
             INSERT INTO tag(name)
             VALUES (%s)
             """,[new_tag])

@sql_connection.connection_handler
def add_user(cursor: RealDictCursor, email:str, hashed_paswword:str) -> int:
    cursor.execute("""
             INSERT INTO users( email, password, registration_time)
             VALUES ((%s),(%s), CURRENT_TIMESTAMP)
             """,[email, hashed_paswword])

@sql_connection.connection_handler
def get_user_id_from_email(cursor: RealDictCursor, email: str) -> int:
    cursor.execute("""
             SELECT id
             FROM users
             WHERE email = (%s) 
             """, [email])
    return cursor.fetchone()['id']

@sql_connection.connection_handler
def get_hashed_password(cursor: RealDictCursor, user_id: int) -> int:
    cursor.execute("""
             SELECT password
             FROM users
             WHERE id = (%s) 
             """, [user_id])
    return cursor.fetchone()['password']


@sql_connection.connection_handler
def get_vote_number_answer(cursor: RealDictCursor, question_id: int, answer_id: int) -> int:
    cursor.execute("""
             SELECT vote_number
             FROM answer
             WHERE question_id =(%s) AND id = (%s)
             """, [question_id, answer_id])
    return cursor.fetchone()['vote_number']

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
def get_question_id_from_comment(cursor: RealDictCursor, comment_id: int) -> list:
    cursor.execute("""
         SELECT question_id
         FROM comment
         WHERE id = (%s)
         """, [comment_id])
    return cursor.fetchall()

@sql_connection.connection_handler
def update_comment(cursor: RealDictCursor, message:str,  comment_id: int,) -> list:
    cursor.execute("""
            UPDATE comment
            SET message = (%s)
            WHERE id = (%s)
            """, [message, comment_id])


@sql_connection.connection_handler
def update_question(cursor: RealDictCursor, title, message, question_id: int) -> list:
    cursor.execute("""
            UPDATE question
            SET title = (%s), message = (%s)
            WHERE id = (%s)
            """, [title, message, question_id])


@sql_connection.connection_handler
def accept_answer(cursor: RealDictCursor, answer_id: int) -> list:
    cursor.execute("""
            UPDATE answer
            SET accepted = True
            WHERE id = (%s)
            """, [answer_id])


@sql_connection.connection_handler
def acceptance_check(cursor: RealDictCursor, question_id: int) -> list:
    cursor.execute("""
            SELECT id
            FROM answer
            WHERE question_id = (%s) AND accepted=TRUE
            """, [question_id])
    return cursor.fetchone()['id']


@sql_connection.connection_handler
def update_answer(cursor: RealDictCursor, answer: str, answer_id: int) -> list:
    cursor.execute("""
            UPDATE answer
            SET message = (%s)
            WHERE id = (%s)
            """, [answer, answer_id])


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

@sql_connection.connection_handler
def answers_for_question_id(cursor: RealDictCursor, user_id: int) -> list:
    query = """
            SELECT answer.*, question.id, question.title
            FROM answer
            LEFT JOIN question
            ON answer.question_id = question.id
            WHERE answer.user_id = %(user_id)s
    """
    args = {'user_id': user_id}
    cursor.execute(query, args)
    return cursor.fetchall()

@sql_connection.connection_handler
def comments_for_question_id(cursor: RealDictCursor, user_id: int) -> list:
    query = """
            SELECT comment.*, question.id, question.title
            FROM comment
            LEFT JOIN question
            ON comment.question_id = question.id
            WHERE comment.user_id = %(user_id)s AND comment.answer_id IS NULL 
    """
    args = {'user_id': user_id}
    cursor.execute(query, args)
    return cursor.fetchall()

@sql_connection.connection_handler
def users_data(cursor: RealDictCursor) -> list:
    query = """
        SELECT *
        FROM users
            """
    cursor.execute(query)
    return cursor.fetchall()