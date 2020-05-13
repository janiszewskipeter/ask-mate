from flask import Flask, render_template, request, redirect
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
    question = []
    for i in data:
        if question_id == i[0]:
            question.append(str(i))
    #question = [i for i in data if question_id == i[0]]
    print(question)
    return render_template('question.html', question=question)



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


@app.route("/question/<question_id>/new-answer")
def add_answer():
    data = connection.get_data('question.csv', PATH)
    return render_template('add_answer.html', data=data)


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
