import pythoncom
from flask import Flask, render_template, request, redirect, url_for
from flaskwebgui import FlaskUI
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

app = Flask(__name__)
input_data = ""

def find_open_apps():
    pythoncom.CoInitialize()  # Initialize the COM library
    apps = []
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() not in apps:
            apps.append(session.Process.name())
    return apps

@app.route('/')
def index_page():
    global input_data
    pythoncom.CoInitialize()  # Initialize the COM library
    apps = find_open_apps()
    for i, app in enumerate(apps):
        if app[-4:] == ".exe":
            apps[i] = app[:-4]

    hello = 200
    return render_template('index.html', apps=apps, hello=hello)  # Pass 'a' as a parameter

@app.route('/submit', methods=['POST'])
def submit():
    global input_data
    input_data = request.form['asd']
    print(input_data)
    return redirect(url_for('index_page'))

if __name__ == '__main__':
    FlaskUI(app=app, server="flask").run()