from contextlib import suppress
from pycaw.magic import MagicApp
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSlider, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QGridLayout, QLabel, QGroupBox, QFileDialog
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from ctypes import cast, POINTER, c_float
from comtypes import CLSCTX_ALL
import numpy as np
import math as math
import os

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Activate the master volume control interface
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.master_volume = cast(interface, POINTER(IAudioEndpointVolume))

        self.setWindowTitle("My App")

        layout = QHBoxLayout()

        self.lowest_volume_limit = self.load_minimum_value()

        # Hard-coded slider
        slider1 = QSlider()
        slider1.valueChanged.connect(lambda value: self.update_master_volume(value))
        layout.addWidget(slider1)

        new_layouts = []
        amount_sliders = 4

        for i in range(amount_sliders):
            lay = QHBoxLayout()
            group_box = QGroupBox(f"Slider {i+1}")
            group_box.setStyleSheet("QGroupBox { border: 1px solid gray; border-radius: 3px; margin-top: 0.5em; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }")
            slider = QSlider()
            slider.valueChanged.connect(lambda value, i=i: self.change_slider(i, value))
            button = QPushButton("Apps")
            button2 = QPushButton("All exe's in folder")
            button.clicked.connect(lambda checked, i=i: self.show_apps(i))
            button2.clicked.connect(lambda checked, i=i: self.allEXE(i))
            lay.addWidget(slider)
            lay.addWidget(button)
            lay.addWidget(button2)
            group_box.setLayout(lay)
            new_layouts.append(group_box)

        for i in range(amount_sliders):
            layout.addWidget(new_layouts[i])

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.apps_window = None
        self.selected_apps = []
        self.slider_apps = [[] for _ in range(amount_sliders)]

        self.load_apps()

        calibrate_button = QPushButton("Calibrate")
        calibrate_button.clicked.connect(self.calibrate_minimum_value)
        layout.addWidget(calibrate_button)
    
    def allEXE(self, slider_index):
        # open a folder selection dialog
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".exe"):
                    self.slider_apps[slider_index].append(os.path.join(root, file))
                    self.selected_apps.append(os.path.join(root, file))

    def show_apps(self, slider_index):
        if self.apps_window is not None:
            self.apps_window.close()

        self.apps_window = QWidget()
        self.apps_window.setWindowTitle("Apps")
        layout = QGridLayout()
        self.apps_window.setGeometry(100, 100, 500, 500)

        vol_label = QLabel("Unselected")
        sel_label = QLabel("Selected")
        vol_group_box = QGroupBox()
        sel_group_box = QGroupBox()
        vol_group_box.setTitle("Unselected")
        sel_group_box.setTitle("Selected")
        vol_layout = QVBoxLayout()
        sel_layout = QVBoxLayout()
        vol_group_box.setLayout(vol_layout)
        sel_group_box.setLayout(sel_layout)

        vol_apps = self.find_open_apps()
        sel_apps = self.slider_apps[slider_index]

        def remove_selected_app(app_index):
            app = sel_apps[app_index]
            sel_apps.remove(app)
            self.selected_apps.remove(app)
            self.apps_window.close()
            self.show_apps(slider_index)

        for i, app in enumerate(vol_apps):
            if app in sel_apps:
                continue
            app_label = QLabel(app)
            app_label.setStyleSheet("QLabel { border: 1px solid gray; padding: 5px; }")
            app_label.mousePressEvent = lambda event, i=i: self.select_app(i, slider_index)
            vol_layout.addWidget(app_label)

        for i, app in enumerate(sel_apps):
            app_label = QLabel(app)
            app_label.setStyleSheet("QLabel { border: 1px solid gray; padding: 5px; }")
            app_label.mousePressEvent = lambda event, i=i: remove_selected_app(i)
            sel_layout.addWidget(app_label)

        # done_button = QPushButton("Done")
        # done_button.clicked.connect(lambda checked, slider_index=slider_index: self.link_apps(slider_index))

        layout.addWidget(vol_group_box, 0, 0)
        layout.addWidget(sel_group_box, 0, 1)

        done_button = QPushButton("Done")
        done_button.clicked.connect(lambda checked, slider_index=slider_index: self.link_apps(slider_index))

        # Add an extra row for the done button
        layout.addWidget(done_button, layout.rowCount(), 0, 1, 2)

        self.apps_window.setLayout(layout)
        self.apps_window.show()

    def find_open_apps(self):
        apps = []
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() not in apps:
                apps.append(session.Process.name())
        return apps

    def select_app(self, app_index, slider_index):
        app = self.find_open_apps()[app_index]
        if app in self.slider_apps[slider_index]:
            self.slider_apps[slider_index].remove(app)
            self.apps_window.layout().itemAtPosition(self.selected_apps.index(app), 1).widget().deleteLater()
            self.selected_apps.remove(app)
        else:
            self.slider_apps[slider_index].append(app)
            app_label = QLabel(app)
            app_label.mousePressEvent = lambda event, i=len(self.selected_apps): self.select_app(i, slider_index)
            self.apps_window.layout().addWidget(app_label, len(self.selected_apps), 1)
            self.selected_apps.append(app)
        
        # Close the current apps window and show it again to refresh the list
        self.apps_window.close()
        self.show_apps(slider_index)
       
    def link_apps(self, slider_index):
        print(f"Slider {slider_index}: {', '.join(self.slider_apps[slider_index])}")
        self.apps_window.close()
        self.save_apps()

    def asd(self, num, in_min, in_max, out_min, out_max):
        return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def change_slider(self, slider_index, value):
        apps = self.slider_apps[slider_index]
        for app in apps:
            self.change_volume(app, self.asd(value, 0, 100, 0, 1))

    def change_volume(self, app, percentage):
        print(app, percentage)
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name() == app:
                volume.SetMasterVolume(percentage, None)

    def find_minimum_value(self):
        volume_level = 0
        while True:
            try:
                hr = self.master_volume.SetMasterVolumeLevel(volume_level, None)
                if hr == 0:
                    volume_level -= 0.01
                else:
                    break
            except Exception as e:
                break
        print(f"Minimum value: {volume_level}")
        return volume_level

    def calibrate_minimum_value(self): # Finds the lowest volume level that the master volume can be set to
        self.lowest_volume_limit = self.find_minimum_value()
        self.save_minimum_value()


    def update_master_volume(self, value):
        volume_level = self.asd(int(value), 0, 100, self.lowest_volume_limit, 0) # Converts the slider value to a volume level

        print(f"Maths: {(np.emath.logn(1.07346, value)) - 65.5582}")
        maths_done = (np.emath.logn(1.07346, value)) - 65.5582 # Does a log function to decode the SetMasterVolumeLevel function
        maths_done = np.clip(maths_done, self.lowest_volume_limit, 0) # Clips the volume level to the lowest volume level so the volume can't go below that

        print(f"Master volume raw: {volume_level}")

        self.master_volume.SetMasterVolumeLevel(int(maths_done), None) # Sets the master volume to the volume level


    def save_apps(self): # saves the apps to a txt file for future use
        with open("apps.txt", "w") as f:
            for apps in self.slider_apps:
                f.write(",".join(apps) + "\n")

    def load_apps(self):
        try:
            with open("apps.txt", "r") as f:
                for i, line in enumerate(f):
                    apps = line.strip().split(",")
                    self.slider_apps[i] = apps
        except FileNotFoundError:
            pass

    def save_minimum_value(self):
        with open("minimum_value.txt", "w") as f:
            f.write(str(self.lowest_volume_limit))

    def load_minimum_value(self):
        try:
            with open("minimum_value.txt", "r") as f:
                return float(f.read())
        except FileNotFoundError:
            return self.find_minimum_value()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
