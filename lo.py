import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSlider, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QGridLayout, QLabel

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        layout = QHBoxLayout()

        new_layouts = []
        amount_sliders = 5

        for i in range(amount_sliders):
            lay = QVBoxLayout()
            slider = QSlider()
            button = QPushButton("Apps")
            button.clicked.connect(lambda checked, i=i: self.show_apps(i))
            lay.addWidget(slider)
            if i != 0:
                lay.addWidget(button)
            new_layouts.append(lay)

        for i in range(amount_sliders):
            layout.addLayout(new_layouts[i])

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.apps_window = None
        self.selected_apps = []
        self.slider_apps = [[] for _ in range(amount_sliders)]

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

        vol_apps = ["App 1", "App 2", "App 3", "App 4", "App 5"]
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

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()