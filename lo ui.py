from contextlib import suppress
from pycaw.magic import MagicApp
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSlider, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QGridLayout, QLabel, QGroupBox
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from ctypes import cast, POINTER, c_float
from comtypes import CLSCTX_ALL
import numpy as np
import math as math

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
            slider.valueChanged.connect(lambda value, i=i+1: self.change_slider(i, value))
            button = QPushButton("Apps")
            button.clicked.connect(lambda checked, i=i+1: self.show_apps(i))
            lay.addWidget(slider)
            lay.addWidget(button)
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

    def show_apps(self, slider_index):
        if self.apps_window is not None:
            self.apps_window.close()

        self.apps_window = QWidget()
        self.apps_window.setWindowTitle("Apps")
        layout = QGridLayout()

        vol_label = QLabel("Vol")
        sel_label = QLabel("Selected")
        layout.addWidget(vol_label, 0, 0)
        layout.addWidget(sel_label, 0, 1)

        vol_apps = self.find_open_apps()
        sel_apps = self.slider_apps[slider_index]

        for i, app in enumerate(vol_apps):
            app_label = QLabel(app)
            app_label.mousePressEvent = lambda event, i=i: self.select_app(i, slider_index)
            layout.addWidget(app_label, i+1, 0)

        for i, app in enumerate(sel_apps):
            app_label = QLabel(app)
            app_label.mousePressEvent = lambda event, i=i: self.select_app(i, slider_index)
            layout.addWidget(app_label, i+1, 1)

        done_button = QPushButton("Done")
        done_button.clicked.connect(lambda checked, slider_index=slider_index: self.link_apps(slider_index))
        layout.addWidget(done_button, len(vol_apps)+1, 0, 1, 2)

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
        app = self.apps_window.layout().itemAtPosition(app_index+1, 0).widget().text()
        if app in self.slider_apps[slider_index]:
            self.slider_apps[slider_index].remove(app)
            self.apps_window.layout().itemAtPosition(self.selected_apps.index(app)+1, 1).widget().deleteLater()
            self.selected_apps.remove(app)
        else:
            self.slider_apps[slider_index].append(app)
            app_label = QLabel(app)
            app_label.mousePressEvent = lambda event, i=len(self.selected_apps): self.select_app(i, slider_index)
            self.apps_window.layout().addWidget(app_label, len(self.selected_apps)+1, 1)
            self.selected_apps.append(app)

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

    def calibrate_minimum_value(self):
        self.lowest_volume_limit = self.find_minimum_value()
        self.save_minimum_value()



    def update_master_volume(self, value):
        volume_level = self.asd(int(value), 0, 100, self.lowest_volume_limit, 0)
        # a = lowest
        # # y = volume level
        # print(f"first log: {np.log(volume_level)}")
        # print(f"second log: {np.log(1.07053)}")
        # print(f"devided: {np.log(volume_level) / np.log(1.07053)}")
        # outputVol = (np.log(volume_level) / np.log(1.07053)) - 68.2409
        # outputVol = floor_log(volume_level, 1.07053) - 68.2409
        print(f"Master volume raw: {volume_level}")
        # print(f"so the volume level is: {outputVol}")
        self.master_volume.SetMasterVolumeLevel(int(volume_level), None)

    def save_apps(self):
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
