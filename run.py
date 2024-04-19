from flask import Flask
from flask import render_template
from flask import request

import sqlite3

from random import choice


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
    n = request.args.get('word')  # id
    try:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        if mode == 'answer':
            query = f'''SELECT word, stress, clar from four WHERE id = {n}'''
            cur.execute(query)
            info = cur.fetchall()[0]
            word = ''
            for i in range(len(info[0])):
                if i == info[1]:
                    word = word + info[0][i].upper()
                else:
                    word = word + info[0][i]
            a = ''
            return render_template('2.html', word=word, clar=(info[2] if info[2] else ''), a=a)
        query = f'''SELECT word, vowels, clar from four WHERE id = {n}'''
        cur.execute(query)
        info = cur.fetchall()[0]
        vowels = list(map(int, info[1].split(';')))
        stress = choice(vowels)
        word = ''
        for i in range(len(info[0])):
            if i == stress:
                word = word + info[0][i].upper()
            else:
                word = word + info[0][i]
        a1 = f'/4?word={choice(range(1, 224))}'
        a2 = f'/4?word={n}&mode=answer'
        return render_template('1.html', word=word, clar=(info[2] if info[2] else ''), a1=a1, a2=a2)
    except sqlite3.Error:
        print('error occurred what a coincidence')
    finally:
        if con:
            con.close()


if __name__ == '__main__':
    app.run(debug=True)
