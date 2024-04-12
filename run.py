from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('1.html')  # https://habr.com/ru/articles/804887/


if __name__ == '__main__':
    app.run(debug=True)
