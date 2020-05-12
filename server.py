from flask import Flask, render_template, request, redirect

app = Flask(__name__)
PATH = app.root_path

@app.route("/")
@app.route("/list")
def list():
    data = # read data function
    return render_template('list.html', data=data)

@app.route("/question/<question_id>")
def question():
    data =  # read data function
    return render_template('question.html', data=data)

@app.route("/add-question>", methods=['POST', 'GET'])
def add_question():

    if request.method == 'POST'
        data =  # read data function

        return render_template('list.html', data=data)

    return render_template('add_question.html', data=data)

@app.route("/question/<question_id>/new-answer")
def add_answer():
    data =  # read data function
    return render_template('add_answer.html', data=data)

@app.route("/question/<question_id>/delete")
def delete():
    data =  # read data function
    return render_template('list.html', data=data)

@app.route("/question/<question_id>/edit")
def edit():
    data =  # read data function
    return render_template('add_question.html', data=data)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )