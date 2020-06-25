from flask import Flask, render_template, request, url_for, redirect, session, escape, flash
import data_manager
import bcrypt

app = Flask(__name__)
PATH = app.root_path

ID = 0
TIME = 1
TITLE = 2
CONTENT = -2


@app.route("/")
@app.route("/index", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        sort_by = request.form['sort_by']
    else:
        sort_by = 'submission_time'
    questions = data_manager.get_first_five_questions(sort_by)
    if 'username' in session:
        logedin = True
        return render_template('index.html', logedin=logedin, questions=questions)
    logedin = False
    return render_template('index.html', logedin=logedin, questions=questions)

@app.route("/users")
def users_list():
    users = data_manager.get_users()
    return render_template('users.html', users=users)

@app.route("/tags")
def tag_list():
    tags = data_manager.get_tags_with_count()
    return render_template('tag_list.html', tags=tags)


@app.route("/list/")
def list():
    questions = data_manager.get_questions()
    return render_template('list.html', questions=questions)

    # @app.route("/search/<filtered_questions>")
    # def search_result(filtered_questions):
    return render_template('index.html', filtered_questions=filtered_questions)


@app.route("/question/<question_id>")
def route_question(question_id):
    if 'username' in session:
        logedin = True
    else:
        logedin = False
    question_id = int(question_id)
    question = data_manager.read_a_question(int(question_id))
    answers_list = data_manager.answer_by_question_id(int(question_id))
    comments = data_manager.get_comments()
    tags = data_manager.get_tags_for_question(question_id)
    try:
        accepted_answer_id = data_manager.acceptance_check(question_id)
    except TypeError:
        accepted_answer_id = -1

    return render_template("question.html", logedin=logedin, comments=comments, question=question, question_id=question_id,
                           answers_list=answers_list, tags=tags, accepted_answer_id=accepted_answer_id)

@app.route("/user/<user_id>",)
def user_page(user_id):
    session['username'] = user_id
    '''
    if 'user_id' not in session:
        flash('You are not logged in!')
        return redirect(url_for('login'))
        '''
    print(session)
    questions_asked = data_manager.questions_by_id(user_id)
    answers = data_manager.answers_for_question_id(user_id)
    comments = data_manager.comments_for_question_id(user_id)
    users_data = data_manager.users_data()
    print(users_data)
    return render_template("user.html", users=users_data, questions_asked=questions_asked, answers=answers, comments=comments)


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        plain_text_password = request.form['password']
        hashed_password = hash_password(plain_text_password)
        data_manager.add_user(email, hashed_password)
        return redirect(url_for("index"))

    return render_template("registration_form.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        try:
            user_id = data_manager.get_user_id_from_email(email)
        except TypeError:
            valid=False
            return render_template('login.html', valid=valid)
        session['username'] = user_id

        plain_text_password = request.form['password']
        hashed_password = data_manager.get_hashed_password(user_id)
        valid = verify_password(plain_text_password, hashed_password)
        if valid:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login', valid=valid))

    return render_template('login.html')

@app.route("/accept/<question_id>/<answer_id>", methods=['POST', 'GET'])
def accept(question_id, answer_id):
    answer_id = int(answer_id)
    data_manager.accept_answer(answer_id)
    return redirect(url_for('route_question', question_id=question_id))

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
    searched_phrase = str(request.form['searched_phrase'])
    filtered_questions = data_manager.search(searched_phrase)
    filtered_answers = data_manager.search_answer(searched_phrase)
    return render_template("search_result.html", questions=filtered_questions, answers=filtered_answers)


@app.route("/question/<question_id>/<tag_name>")
def tag_delete(question_id, tag_name):
    tag_id = data_manager.get_tag_id(tag_name)
    data_manager.delete_tag_from_question(question_id, tag_id)
    return redirect(url_for('route_question', question_id=question_id))


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

@app.route("/question/<question_id>/new-answer/<answer_id>", methods=['POST', 'GET'])
def add_answer(question_id, answer_id):
    question_id = int(question_id)
    answer_id = int(answer_id)
    if request.method == 'POST':
        answer = request.form['answer']
        if answer_id == -1:
            data_manager.save_answer(answer, question_id)
        else:
            data_manager.update_answer(answer, answer_id)
        return redirect(url_for('route_question', question_id=question_id))

    try:
        answer = data_manager.get_answer_by_id(answer_id)[0]
    except IndexError:
        answer = data_manager.get_answer_by_id(answer_id)
    return render_template('add_answer.html', answer=answer, question_id=question_id, answer_id=answer_id)


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

@app.route("/question/<question_id>/<comment_id>/edit-comment", methods=['POST', 'GET'])
def edit_comment(question_id, comment_id ):
    if request.method == 'POST':
        message = request.form['comment']
        data_manager.update_comment(message,comment_id)
        return redirect(url_for('route_question', question_id=question_id))

    question = data_manager.get_question_by_id(question_id)
    comment = data_manager.get_comment_by_id(comment_id)[0]
    edit = True
    return render_template('add_comment.html', question=question, question_id=question_id, comment_id=comment_id, comment=comment, edit=edit )

'''
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
'''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index', logedin=False))


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=5050,
        debug=True,
    )