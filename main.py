from project import search
import sqlite3
from flask import Flask, request, render_template
app = Flask(__name__)

con = sqlite3.connect('тексты (3).bd')
cur = con.cursor()


@app.route('/')
def my_form():
    return render_template('main.html')


@app.route('/search', methods=['post'])
def my_form_post():
    variable = request.form['variable']
    search_exp = str(variable)
    result = search(search_exp)
    return render_template('search.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)