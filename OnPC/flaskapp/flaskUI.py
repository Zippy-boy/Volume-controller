from flask import Flask, render_template, request, redirect, url_for
from flaskwebgui import FlaskUI

app = Flask(__name__)
input_data = ""

@app.route('/')
def index_page():
    global input_data
    a = "hello"
    hello = 200
    return render_template('index.html', a=input_data, hello=hello)  # Pass 'a' as a parameter

@app.route('/submit', methods=['POST'])
def submit():
    global input_data
    input_data = request.form['asd']
    print(input_data)
    return redirect(url_for('index_page'))

if __name__ == '__main__':
    FlaskUI(app=app, server="flask").run()