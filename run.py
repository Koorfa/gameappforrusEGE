from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('1.html')  # https://habr.com/ru/articles/804887/


# https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask-ru
@app.route('/query-example')
def query_example():
    # if key doesn't exist, returns None
    language = request.args.get('language')

    return '''<h1>The language value is: {}</h1>'''.format(language)


@app.route('/4')
def task4():
    mode = request.args.get('mode')  # question/answer
    # if key doesn't exist, request.args.get() returns None
    # while request.args[] returns error 400
    word = request.args.get('word')  # id
    answer = request.args.get('answer')  # right/wrong
    if mode == 'answer':
        return None
    return render_template('1.html', word=word)


if __name__ == '__main__':
    app.run(debug=True)
