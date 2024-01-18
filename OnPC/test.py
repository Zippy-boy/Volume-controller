import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSlider, QPushButton, QVBoxLayout, QListWidget, QHBoxLayout, QStackedWidget, QComboBox
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from ctypes import cast, POINTER, c_float
from comtypes import CLSCTX_ALL

class VolumeController:
    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.master_volume = cast(self.interface, POINTER(IAudioEndpointVolume))
        self.lowest_volume_limit = self.find_minimum_value()

    def change_volume(self, app, percentage):
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
        return volume_level

    def update_master_volume(self, value):
        volume_level = self.asd(int(value), 0, 100, self.lowest_volume_limit, 0)
        self.master_volume.SetMasterVolumeLevel(int(volume_level), None)

    def asd(self, num, in_min, in_max, out_min, out_max):
        return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Create an instance of the VolumeController class
volume_controller = VolumeController()

def update_app_volume(value, slider, app_combobox):
    app_name = app_combobox.currentText()
    if app_name != "None":
        volume_controller.change_volume(app_name, volume_controller.asd(slider.value(), 0, 100, 0, 1))


def main():
    app = QApplication(sys.argv)
    
    # Create the main window
    main_window = QMainWindow()
    main_window.setWindowTitle("Volume Mixer App")
    
    # Create a central widget
    central_widget = QWidget(main_window)
    main_window.setCentralWidget(central_widget)
    
    # Create a stacked widget for switching screens
    stacked_widget = QStackedWidget()
    
    # Create the first screen with volume sliders and app buttons
    volume_screen1 = QWidget()
    slider1 = QSlider()
    
    app_button1 = QComboBox()  # ComboBox for selecting the app for slider1
    
    volume_layout1 = QVBoxLayout()
    volume_layout1.addWidget(slider1)
    volume_layout1.addWidget(app_button1)
    volume_screen1.setLayout(volume_layout1)
    
    # Create the second screen with volume sliders and app buttons
    volume_screen2 = QWidget()
    slider2 = QSlider()
    
    app_button2 = QComboBox()  # ComboBox for selecting the app for slider2
    
    volume_layout2 = QVBoxLayout()
    volume_layout2.addWidget(slider2)
    volume_layout2.addWidget(app_button2)
    volume_screen2.setLayout(volume_layout2)
    
    # Create the third screen for managing apps (without a master volume slider)
    app_screen = QWidget()
    deselected_apps = QListWidget()
    selected_apps = QListWidget()
    
    app_layout = QHBoxLayout()
    app_layout.addWidget(deselected_apps)
    app_layout.addWidget(selected_apps)
    app_screen.setLayout(app_layout)
    
    # Create buttons for switching screens
    volume_button1 = QPushButton("Slider 1")
    volume_button2 = QPushButton("Slider 2")
    app_button = QPushButton("Apps")
    
    def switch_to_volume1():
        stacked_widget.setCurrentWidget(volume_screen1)
    
    def switch_to_volume2():
        stacked_widget.setCurrentWidget(volume_screen2)
    
    def switch_to_apps():
        stacked_widget.setCurrentWidget(app_screen)
    
    volume_button1.clicked.connect(switch_to_volume1)
    volume_button2.clicked.connect(switch_to_volume2)
    app_button.clicked.connect(switch_to_apps)
    
    # Connect volume sliders to update app volumes
    slider1.valueChanged.connect(lambda value: update_app_volume(value, slider1, app_button1))
    slider2.valueChanged.connect(lambda value: update_app_volume(value, slider2, app_button2))

    
    # Connect app buttons to update app volumes
    app_button1.currentIndexChanged.connect(lambda index: update_app_volume(slider1.value(), slider1, app_button1))
    app_button2.currentIndexChanged.connect(lambda index: update_app_volume(slider2.value(), slider2, app_button2))
    
    # Add screens to the stacked widget
    stacked_widget.addWidget(volume_screen1)
    stacked_widget.addWidget(volume_screen2)
    stacked_widget.addWidget(app_screen)
    
    # Add widgets to the central widget
    central_layout = QVBoxLayout()
    central_layout.addWidget(volume_button1)
    central_layout.addWidget(volume_button2)
    central_layout.addWidget(app_button)
    central_layout.addWidget(stacked_widget)
    central_widget.setLayout(central_layout)
    
    # Show the main window
    main_window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()