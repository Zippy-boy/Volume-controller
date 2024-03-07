from flask import Flask, render_template
from flaskwebgui import FlaskUI

app = Flask(__name__)

@app.route('/')
def index_page():
    a = "hello"
    return render_template('index.html', a=a)  # Pass 'a' as a parameter

if __name__ == '__main__':
    FlaskUI(app=app, server="flask").run()