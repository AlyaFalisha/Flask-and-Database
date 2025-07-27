print("hello")
from random import randint
from flask import Flask, session, redirect, url_for
from db_scripts import get_question_after
def index():
    global quiz, last_question
    max_quiz = 3
    quiz = randint(1, max_quiz)
    last_question = 0
    return '<a href="/test">Test</a>'
def test():
    global last_question
    result = get_question_after(last_question, quiz)
    if result is None or len(result) == 0:
        return redirect(url_for('result'))
    else:
        last_question = result[0]
        return'<h1>'+str(quiz)+'<br>'+str(result)+'</h1>'
def result():
    return "done"
app = Flask(__name__)
app.add_url_rule('/', 'index', index)
app.add_url_rule('/test','test', test)
app.add_url_rule('/result','result', result)

if __name__=='__main__':
    app.run()