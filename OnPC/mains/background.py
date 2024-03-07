import pystray
from PIL import Image
import os
import subprocess


def open_action(icon, item):
    ui_exe_path = "C:/Users/Zippy/Documents/GitHub/Volume-controller/output/UI/UI.exe"
    subprocess.Popen(ui_exe_path)

def quit_action(icon, item):
    icon.stop()

image = Image.open("C:/Users/Zippy/Documents/GitHub/Volume-controller/OnPC/mains/icon.png")

icon = pystray.Icon(name='Volume Controller', icon=image, title='Volume controller')

menu = (
    pystray.MenuItem('Open', open_action),
    pystray.MenuItem('Quit', quit_action),
)

icon.menu = pystray.Menu(*menu)
icon.on_click = open_action
icon.run()