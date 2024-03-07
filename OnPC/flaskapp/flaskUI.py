import pythoncom
from flask import Flask, render_template, request, redirect, url_for
from flaskwebgui import FlaskUI
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

app = Flask(__name__)
with open("sliders.txt", "r") as file:
    datas = file.read()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
master_volume = cast(interface, POINTER(IAudioEndpointVolume))


def change_volume(app, percentage):
    print(app, percentage)
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == app:
            volume.SetMasterVolume(percentage, None)

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
    pythoncom.CoInitialize()  # Initialize the COM library
    apps = find_open_apps()
    with open("sliders.txt", "r") as file:
        input_data = file.read()
        input_data = input_data.split("},")
        for da in input_data:
            print(da)
        slider1Apps = input_data[0]
        print(slider1Apps)
        slider2Apps = []
        slider3Apps = []
        slider4Apps = []
    return render_template('index.html', apps=apps)  # Pass 'a' as a parameter

@app.route('/submit', methods=['POST'])
def submit():
    global datas
    # read all the insides of the divs with .appBox
    input_data = request.get_json()
    for data in input_data:
        print(data)
    datas = input_data
    with open("sliders.txt", "w") as file:
        file.write(str(datas))
    return redirect(url_for('index_page'))

@app.route('/change_volume', methods=['POST'])
def change_volume_route():
    input_data = request.get_json()
    slider_index = input_data['slider']
    percentage = input_data['volume']
    print(datas[int(slider_index)-1]['apps'])
    for app in datas[int(slider_index)-1]['apps']:
        print(app, percentage)
        change_volume(app, percentage)
    # print(apps)
    return redirect(url_for('index_page'))

if __name__ == '__main__':
    FlaskUI(app=app, server="flask").run()