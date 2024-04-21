from flask import Flask
from flask import render_template
from flask import request

import sqlite3

from random import choice


app = Flask(__name__)


# https://habr.com/ru/articles/804887/
# https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask-ru


@app.route('/4')
def task4():
    mode = request.args.get('mode')  # question/answer
    # if key doesn't exist, request.args.get() returns None
    # while request.args[] returns error 400
    n = request.args.get('word')  # id
    s = request.args.get('s')
    flag = False
    try:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        if s:
            query = f"""SELECT stress from four WHERE id = {n}"""
            cur.execute(query)
            stress = int(cur.fetchall()[0][0])
            for i in range(len(s)):
                if s[i].isupper():
                    if i == stress:
                        flag = True
                        break
            if flag:
                n = choice(range(1, 222))
        if mode == 'answer' or s and not flag:
            query = f'''SELECT word, stress, clar from four WHERE id = {n}'''
            cur.execute(query)
            info = cur.fetchall()[0]
            word = ''
            for i in range(len(info[0])):
                if i == info[1]:
                    word = word + info[0][i].upper()
                else:
                    word = word + info[0][i]
            a = f'/4?word={choice(range(1, 222))}'
            return render_template('2.html', word=word, clar=(info[2] if info[2] else ''), a=a)
        query = f'''SELECT word, vowels, clar from four WHERE id = {n}'''
        cur.execute(query)
        info = cur.fetchall()[0]
        con.close()
        vowels = list(map(int, info[1].split(';')))
        stress = choice(vowels)
        word = ''
        for i in range(len(info[0])):
            if i == stress:
                word = word + info[0][i].upper()
            else:
                word = word + info[0][i]
        if 'ё' in word:
            word = word.replace('ё', 'е')
        a1 = f'/4?word={n}&s={word}'
        a2 = f'/4?word={n}&mode=answer'
        return render_template('1.html', word=word, clar=(info[2] if info[2] else ''), a1=a1, a2=a2)
    except sqlite3.Error:
        print(sqlite3.Error)


if __name__ == '__main__':
    app.run(debug=True)
