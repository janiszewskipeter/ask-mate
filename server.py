from flask import Flask, render_template, request, redirect, url_for
import connection
import util

app = Flask(__name__)
PATH = app.root_path


@app.route("/")
@app.route("/list")
def list():
    data = connection.get_data('question.csv', PATH)

    return render_template('list.html', data=data)


@app.route("/question/<question_id>")
def question(question_id):
    data = connection.get_data('question.csv', PATH)
    for i in data:
        if question_id == i[0]:
            question = i
    answer= "koczkodan"
    #question = [i for i in data if question_id == i[0]]
    return render_template('question.html', question=question, question_id=question_id, answer=answer)


@app.route("/add_question", methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        id = util.id_generator()
        submission_time = util.get_time()
        # view_number = request.form[]
        # vote_number = request.form[]
        title = request.form['question_title']
        message = request.form['question']
        # image = request.form[]

        data_to_save = [submission_time,title,message, id, "image"]
        connection.save_data(PATH, 'question.csv', data_to_save)
        data = connection.get_data('question.csv', PATH)
        return render_template('list.html', data=data)

    return render_template('add_question.html')


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def add_answer(question_id):
    if request.method == 'POST':
        data = connection.get_data('answer.csv', PATH)
        question_data = connection.get_data('question.csv', PATH)
        question = [q for q in question_data if question_data[0] == question_id]
        answer = request.form['answer']
        answer_to_save = [question_id, answer]
        connection.save_data(PATH, 'answer.csv', answer_to_save)
        return render_template('question.html', answer_to_save=answer_to_save, data=data)
    data = connection.get_data('answer.csv', PATH)
    question_data = connection.get_data('question.csv', PATH)
    print("hello")
    question = "tyguhij"#[q for q in question_data if question_data[0] == question_id]
    answer = "avshjk" #[q for q in data if data[0] == question_id]
    return render_template('add_answer.html', question=question, answer=answer)

@app.route("/question/<question_id>/delete")
def delete():
    data = connection.get_data('question.csv', PATH)
    return render_template('list.html', data=data)


@app.route("/question/<question_id>/edit")
def edit():
    data = connection.get_data('question.csv', PATH)
    return render_template('add_question.html', data=data)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5050,
        debug=True,
    )
#id,submission_time,vote_number,question_id,message,image
