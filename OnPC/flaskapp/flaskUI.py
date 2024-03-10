import pythoncom
from flask import Flask, render_template, request, redirect, url_for
from flaskwebgui import FlaskUI
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import json

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
            # print(da)
            pass
        slider1Apps = input_data[0]
        # print(slider1Apps)
        slider2Apps = []
        slider3Apps = []
        slider4Apps = []
    return render_template('index.html', apps=apps)  # Pass 'a' as a parameter

@app.route('/submit', methods=['POST'])
def submit():
    input_data = request.get_json()
    newSliderDict = []
    # print(input_data[0])
    for slider in input_data:
        apps = slider['apps']
        slider = slider['slider']
        newApps = []
        # print(slider, apps)
        for app in apps:
            newApps.append(app.replace("\n", "").replace(" ", ""))
        # print(newApps)
        newSliderDict.append({
            "slider": slider,
            "apps": newApps
        })
    
    print(json.dumps(newSliderDict))
    with open("sliders.txt", "w") as file:
        file.write(str(json.dumps(newSliderDict)))
    return redirect(url_for('index_page'))

@app.route('/change_volume', methods=['POST'])
def change_volume_route():
    input_data = request.get_json()
    slider_index = input_data['slider']
    percentage = input_data['volume']
    with open("sliders.txt", "r") as file:
        file = file.readline().replace("]", "").replace("[", "").split("},")
        print(file[0])
        
        for app in file[0]["slider": slider_index]["apps"]:

            print(app, percentage)
            # change_volume(app, percentage)
        # print(apps)
        return redirect(url_for('index_page'))

if __name__ == '__main__':
    FlaskUI(app=app, server="flask").run()