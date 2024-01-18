from __future__ import print_function
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSlider, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QGridLayout, QLabel, QGroupBox
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from ctypes import cast, POINTER, c_float
from comtypes import CLSCTX_ALL
import serial 

global slider_apps
slider_apps = [[] for _ in range(4)]

def load_apps():
    try:
        with open("apps.txt", "r") as f:
            app_names = f.read().splitlines()
            for i, app_name in enumerate(app_names):
                slider_apps[i] = [app_name]
    except FileNotFoundError:
        pass

load_apps()

def change_slider(slider_index, value):
    apps = slider_apps[slider_index]
    for app in apps:
        change_volume(app, asd(value, 0, 100, 0, 1))

def change_volume(app, percentage):
    print(app, percentage)
    if percentage <=0.02:
        percentage = 0
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == app:
            volume.SetMasterVolume(percentage, None)

def find_minimum_value():
    volume_level = 0
    while True:
        try:
            hr = master_volume.SetMasterVolumeLevel(volume_level, None)
            if hr == 0:
                volume_level -= 0.01
            else:
                break
        except Exception as e:
            break
    print(f"Minimum value: {volume_level}")
    return volume_level

def calibrate_minimum_value():
    lowest_volume_limit = find_minimum_value()
    save_minimum_value()

def update_master_volume(value, lowest_volume_limit):
    volume_level = asd(int(value), 0, 100, lowest_volume_limit, 0)
    master_volume.SetMasterVolumeLevel(int(volume_level), None)

def asd(num, in_min, in_max, out_min, out_max):
    return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def save_minimum_value(self):
    with open("minimum_value.txt", "w") as f:
        f.write(str(self.lowest_volume_limit))

def load_minimum_value(self):
    try:
        with open("minimum_value.txt", "r") as f:
            return float(f.read())
    except FileNotFoundError:
        return self.find_minimum_value()

# activate the master volume control interface
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
master_volume = cast(interface, POINTER(IAudioEndpointVolume))


ser = serial.Serial('COM5')
values = ser.readline().decode('utf-8').strip().split(',')
nob1_pre, nob2_pre, nob3_pre = int(values[0]), int(values[1]), int(values[2])

# get all audio sessions
sessions = AudioUtilities.GetAllSessions()

# read app names from file
with open('apps.txt', 'r') as f:
    app_names = f.read().splitlines()

# activate the volume control interface for each app
app_volumes = {}
for lin in app_names:
    ay = lin.split(',')
    for session in sessions:
        try:
            if session.Process and session.Process.name() == ay[0]:
                app_volumes[ay[0]] = session._ctl.QueryInterface(ISimpleAudioVolume)
                break
        except:
            pass

print(app_volumes)

# read data from serial and update volumes accordingly
while True:
    # read data from serial and parse values
    values = ser.readline().decode('utf-8').strip().split(',')
    # print(values)
    if len(values) != 3:
        continue
    nob2, nob1, nob3 = int(values[0]), int(values[1]), int(values[2])
    if nob2 == 1: nob2 = 0

    # update master volume
    if nob1 != nob1_pre:
        if nob1+1 != nob1_pre and nob1-1 != nob1_pre:
            print("main vol: " + str(nob1))
            master_volume_level = asd(nob1, 0, 100, 0, -37)
            master_volume.SetMasterVolumeLevel(int(master_volume_level), None)
            nob1_pre = nob1

    # update app volumes
    for app_name, app_volume in app_volumes.items():
        print(app_name, nob2, nob2_pre)
        if nob2 != nob2_pre:
            if nob2+1 != nob2_pre and nob2-1 != nob2_pre:
                print(f"{app_name}: " + str(nob2))
                app_volume_level = asd(nob2, 0, 100, 0, 1)
                change_volume(app_name, app_volume_level)

    # time.sleep(0.01)