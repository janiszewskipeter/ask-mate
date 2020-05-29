from flask import Flask, render_template, request, url_for, redirect
import connection
import util
import data_manager

app = Flask(__name__)
PATH = app.root_path

ID = 0
TIME = 1
TITLE = 2
CONTENT = -2


@app.route("/")
@app.route("/index")
def index():
    questions = data_manager.get_first_five_questions()
    return render_template('index.html', questions=questions)

@app.route("/list")
def list():
    questions = data_manager.get_questions()
    return render_template('list.html', questions=questions)


@app.route("/question/<question_id>")
def route_question(question_id):
    question = data_manager.read_a_question(int(question_id))
    answers_list = data_manager.answer_by_question_id(int(question_id))
    comments = data_manager.get_comment_by_question_id(question_id)

    return render_template("question.html", comments=comments, question=question, question_id=question_id, answers_list=answers_list)


@app.route("/add_question", methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        id_ = data_manager.get_new_question_id()
        submission_time = data_manager.convert_time(data_manager.get_current_unix_timestamp())
        title = request.args.get('title')
        message = request.args.get('message')
        views = 0
        votes = 0
        question_dict = {
            'id': id_,
            'submission_time': submission_time,
            'view_number': views,
            'vote_number': votes,
            'title': title,
            'message': message,
            'image': None
        }
        data_manager.add_question(question_dict)
    return render_template('add_question.html')


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def add_answer(question_id):
    if request.method == 'POST':
        answers = connection.get_data('answer.csv', PATH)
        question_data = connection.get_data('question.csv', PATH)
        question = [q for q in question_data if question_data[0] == question_id]
        answer = request.form['answer']
        answer_to_save = [question_id, answer]

        answers.append(answer_to_save)
        connection.save_data(PATH, 'answer.csv', answer_to_save, 'a')

        return redirect(url_for('route_question', question_id=question_id))

    answers = connection.get_data('answer.csv', PATH)
    question_data = connection.get_data('question.csv', PATH)
    question = [q for q in question_data if question_data[0] == question_id]
    answer = [a for a in answers if answers[0] == question_id]
    return render_template('add_answer.html', question=question, answer=answer, question_id=question_id, )


@app.route("/question/<question_id>/<answer_id>/new-comment", methods=['POST', 'GET'])
def add_comment(question_id, answer_id):
    question_id = int(question_id)
    answer_id = int(answer_id)
    if request.method == 'POST':
        if answer_id == -1:
            edited_count = 0
            message = request.form['comment']
            data_manager.add_comment_to_qustion(message=message, question_id=question_id, edited_count=edited_count)
            return redirect(url_for('route_question', question_id=question_id))
        else:
            edited_count = 0
            message = request.form['comment']
            data_manager.add_comment_to_answer(message=message, answer_id=answer_id, edited_count=edited_count)
            return redirect(url_for('route_question', question_id=question_id))

    return render_template('add_comment.html', question_id=question_id, answer_id=answer_id)

@app.route("/question/<question_id>/delete")
def delete():
    data = connection.get_data('question.csv', PATH)
    return render_template('list.html', data=data)


@app.route("/question/<question_id>/edit", methods=['POST', 'GET'])
def edit(question_id):
    edit = True
    if request.method == 'POST':
        id = question_id
        # view_number = request.form[]
        # vote_number = request.form[]
        title = request.form['question_title']
        message = request.form['question']
        # image = request.form[]

        questions = connection.get_data('question.csv', PATH)
        index = questions.index([q for q in questions if q[ID] == question_id][0])
        submission_time = questions[index][TIME]
        questions[index] = [id, submission_time, title, message, "image"]

        connection.save_edited_data(PATH, 'question.csv', questions, 'w')

        return redirect(url_for('question', question_id=question_id))

    questions = connection.get_data('question.csv', PATH)
    question = [q for q in questions if q[0] == question_id][0]

    return render_template('add_question.html', edit=edit, question_id=question_id, question=question, TITLE=TITLE,
                           CONTENT=CONTENT)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5050,
        debug=True,
    )
#id,submission_time,vote_number,question_id,message,image
