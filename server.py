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


@app.route("/list/")
def list():
    questions = data_manager.get_questions()
    return render_template('list.html', questions=questions)

    # @app.route("/search/<filtered_questions>")
    # def search_result(filtered_questions):
    return render_template('index.html', filtered_questions=filtered_questions)


@app.route("/question/<question_id>")
def route_question(question_id):
    question_id = int(question_id)
    question = data_manager.read_a_question(int(question_id))
    answers_list = data_manager.answer_by_question_id(int(question_id))
    comments = data_manager.get_comments()
    tags = data_manager.get_tags_for_question(question_id)

    return render_template("question.html", comments=comments, question=question, question_id=question_id,
                           answers_list=answers_list, tags=tags)


@app.route("/vote/<question_id>/<answer_id>")
def vote(question_id, answer_id):
    question_id = int(question_id)
    answer_id = int(answer_id)
    if answer_id == -1:
        votes = data_manager.get_vote_number(question_id)
        try:
            votes = votes + 1
        except TypeError:
            votes = 1
        data_manager.vote(votes, question_id)
        return redirect(url_for('route_question', question_id=question_id))
    else:
        votes = data_manager.get_vote_number_answer(question_id, answer_id)
        try:
            votes = votes + 1
        except TypeError:
            votes = 1
        data_manager.vote_answer(votes, question_id, answer_id)
        return redirect(url_for('route_question', question_id=question_id))


@app.route("/search", methods=['POST', 'GET'])
def search():
    searched_phrase = request.form['searched_phrase']
    filtered_questions = data_manager.search(searched_phrase)

    return render_template("index.html", questions=filtered_questions)


@app.route("/question/<question_id>/new-tag", methods=['POST', 'GET'])
def add_tag(question_id):
    if request.method == 'POST':

        try:
            tag = request.form['tag']
        except KeyError:
            tag = None
        try:
            new_tag = request.form['new_tag']
        except KeyError:
            new_tag = None

        if new_tag == None:
            tag_id = tag
            data_manager.add_tag_to_question(question_id, tag_id)
            return redirect(url_for('route_question', question_id=question_id))
        else:
            data_manager.add_new_tag(new_tag)
            tags = data_manager.get_tags()
            return render_template("tags.html", question_id=question_id, tags=tags)

    tags = data_manager.get_tags()
    return render_template("tags.html", question_id=question_id, tags=tags)


@app.route("/delete/<question_id>/<answer_id>/<comment_id>")
def delete(question_id, answer_id, comment_id):
    question_id = int(question_id)
    answer_id = int(answer_id)
    comment_id = int(comment_id)
    if question_id != -1 and answer_id == -1 and comment_id == -1:
        data_manager.delete_question(question_id)
        return redirect(url_for('route_question', question_id=question_id))
    if answer_id != -1 and comment_id == -1:
        data_manager.delete_answer(question_id, answer_id)
        return redirect(url_for('route_question', question_id=question_id))
    if comment_id != -1 and answer_id != -1:
        data_manager.delete_answer_comment(answer_id)
        return redirect(url_for('route_question', question_id=question_id))
    if comment_id != -1 and answer_id == -1:
        data_manager.delete_question_comment(question_id, comment_id)
        return redirect(url_for('route_question', question_id=question_id))
    return redirect(url_for('index'))


@app.route("/add_question/<question_id>", methods=['POST', 'GET'])
def add_question(question_id):
    question_id = int(question_id)
    if request.method == 'POST':
        title = request.form['question_title']
        message = request.form['question']
        if question_id == -1:
            data_manager.add_question(title, message)
        else:
            data_manager.update_question(title, message, question_id)
        return redirect(url_for('list'))

    question = data_manager.get_question_by_id(question_id)
    return render_template('add_question.html', question_id=question_id, question=question)


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def add_answer(question_id):
    if request.method == 'POST':
        answer = request.form['answer']
        data_manager.save_answer(answer, question_id)

        return redirect(url_for('route_question', question_id=question_id))

    answers = data_manager.get_answer_by_question_id(question_id)
    question = data_manager.get_question_by_id(question_id)
    return render_template('add_answer.html', question=question, question_id=question_id, )


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
        host='0.0.0.1',
        port=5050,
        debug=True,
    )
