import tkinter as tk
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from ctypes import cast, POINTER, c_float
from comtypes import CLSCTX_ALL
import psutil
import win32gui

# Activate the master volume control interface
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
master_volume = cast(interface, POINTER(IAudioEndpointVolume))

# Function to change volume for selected app
def change_volume(app, percentage):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == app:
            volume.SetMasterVolume(percentage, None)

# Function to find all open applications
def find_open_apps():
    apps = []
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() not in apps:
            apps.append(session.Process.name())
    return apps

# Function to update volume for selected app
def update_app_volume1(value):
    app_name = app_var1.get()
    if app_name != "None":
        change_volume(app_name, asd(int(app_volume_slider1.get()), 0, 100, 0, 1))

def update_app_volume2(value):
    app_name = app_var2.get()
    if app_name != "None":
        change_volume(app_name, asd(int(app_volume_slider2.get()), 0, 100, 0, 1))

def asd(num, in_min, in_max, out_min, out_max):
    return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Function to refresh app selection dropdown menus
def refresh_apps():
    app_menu1['menu'].delete(0, 'end')
    app_menu2['menu'].delete(0, 'end')
    for app in find_open_apps():
        app_menu1['menu'].add_command(label=app, command=tk._setit(app_var1, app))
        app_menu2['menu'].add_command(label=app, command=tk._setit(app_var2, app))

# Create a Tkinter application window
root = tk.Tk()
root.title("Volume Control")

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

lowest_volume_limit = find_minimum_value()

# Function to update master volume
def update_master_volume(value):
    volume_level = asd(int(value), 0, 100, lowest_volume_limit, 0)
    master_volume.SetMasterVolumeLevel(int(volume_level), None)

# Create labels for volume controls
master_volume_label = tk.Label(root, text="Master Volume:")
app_label1 = tk.Label(root, text="Select App 1:")
app_label2 = tk.Label(root, text="Select App 2:")

# Create dropdown menu for app selection
app_var1 = tk.StringVar(root)
app_var1.set("None")
app_menu1 = tk.OptionMenu(root, app_var1, *find_open_apps(), command=update_app_volume1)

app_var2 = tk.StringVar(root)
app_var2.set("None")
app_menu2 = tk.OptionMenu(root, app_var2, *find_open_apps(), command=update_app_volume2)

# Create volume control sliders
master_volume_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Master", command=update_master_volume)
app_volume_slider1 = tk.Scale(root, from_=0, to=100, orient="horizontal", label="App 1", command=update_app_volume1)
app_volume_slider2 = tk.Scale(root, from_=0, to=100, orient="horizontal", label="App 2", command=update_app_volume2)

# Create refresh button
refresh_button = tk.Button(root, text="Refresh", command=refresh_apps)

# Pack the widgets
master_volume_label.pack()
master_volume_slider.pack()
app_label1.pack()
app_menu1.pack(side="left")
app_volume_slider1.pack(side="left")
app_label2.pack()
app_menu2.pack(side="left")
app_volume_slider2.pack(side="left")
refresh_button.pack()

# Run the Tkinter main loop
root.mainloop()