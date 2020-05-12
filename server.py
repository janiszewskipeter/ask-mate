from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
@app.route("/list")
def list():
    data = # read data function
    return render_template('list.html', data=data)

@app.route("/question/<question_id>")
def question():
    data =  # read data function
    return render_template('question.html', data=data)

@app.route("/add-question>")
def add_question():
    data =  # read data function
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
    app.run()
