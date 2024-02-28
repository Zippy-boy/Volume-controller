import pystray
from PIL import Image
import os
import subprocess

def on_icon_click(icon, item):
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the UI.exe file
    ui_exe_path = "C:/Users/Zippy/Documents/GitHub/Volume-controller/output/UI/UI.exe"
    
    # Launch the UI.exe
    subprocess.Popen(ui_exe_path)

def open_action(icon, item):
    # Path to the UI.exe file
    ui_exe_path = "C:/Users/Zippy/Documents/GitHub/Volume-controller/output/UI/UI.exe"
    
    # Launch the UI.exe
    subprocess.Popen(ui_exe_path)

def quit_action(icon, item):
    icon.stop()

image = Image.open("C:/Users/Zippy/Documents/GitHub/Volume-controller/OnPC/mains/icon.png")

# Create the system tray icon
icon = pystray.Icon(name='MyApp', icon=image, title='Volume controller')

# Create the menu
menu = (
    pystray.MenuItem('Open', open_action),
    pystray.MenuItem('Quit', quit_action),
)

# Set the menu for the icon
icon.menu = pystray.Menu(*menu)

# Set the click event handler
icon.on_click = on_icon_click

# Run the icon
icon.run()
