import tkinter as tk
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from ctypes import cast, POINTER, c_float
from comtypes import CLSCTX_ALL


def change_volume(app, percentage):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == app:
            volume.SetMasterVolume(percentage, None)

def asd(num, in_min, in_max, out_min, out_max):
    return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Create a Tkinter application window
root = tk.Tk()
root.title("Volume Control")

# Function to update master volume
def update_master_volume(value):
    volume_level = asd(int(value), 0, 100, -61, 0)
    master_volume.SetMasterVolumeLevel(int(volume_level), None)

# Function to update Spotify volume
def update_spotify_volume(value):
    change_volume("Spotify.exe", asd(int(value), 0, 100, 0, 1))

# Function to update Discord volume
def update_discord_volume(value):
    change_volume("Discord.exe", asd(int(value), 0, 100, 0, 1))

# Create labels for volume controls
master_volume_label = tk.Label(root, text="Master Volume:")
spotify_volume_label = tk.Label(root, text="Spotify Volume:")
discord_volume_label = tk.Label(root, text="Discord Volume:")

# Create volume control sliders
master_volume_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Master", command=update_master_volume)
spotify_volume_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Spotify", command=update_spotify_volume)
discord_volume_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Discord", command=update_discord_volume)

# Pack the widgets
master_volume_label.pack()
master_volume_slider.pack()
spotify_volume_label.pack()
spotify_volume_slider.pack()
discord_volume_label.pack()
discord_volume_slider.pack()

# Activate the master volume control interface
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
master_volume = cast(interface, POINTER(IAudioEndpointVolume))

# Run the Tkinter main loop
root.mainloop()