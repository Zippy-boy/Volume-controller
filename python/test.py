from __future__ import print_function
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import serial
import math
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume


def spotify(persentage):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "Spotify.exe":
            print("volume.GetMasterVolume(): %s" % volume.GetMasterVolume())
            volume.SetMasterVolume(persentage, None)


# activate the master volume control interface
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# get all audio sessions
sessions = AudioUtilities.GetAllSessions()

# find the Spotify session
spotify_session = None
for session in sessions:
    try:
        if session.Process and session.Process.name() == 'Spotify.exe':
            spotify_session = session
            break
    except:
        pass

# activate the Spotify volume control interface
if spotify_session is not None:
    spotify_volume = spotify_session._ctl.QueryInterface(ISimpleAudioVolume)

# get the current master volume
master_volume = volume.GetMasterVolumeLevel()
# the spotify volume is relative to the master volume so we need to calculate the difference
spotify_volume_diff = spotify_volume.GetMasterVolume() - master_volume
# set the spotify volume
spotify_volume.SetMasterVolume(spotify_volume_diff, None)


def asd(num, in_min, in_max, out_min, out_max):
    return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


# volume.SetMasterVolumeLevel(-37, None)

# open serial port
ser = serial.Serial('COM4')

# read data from serial and update volumes accordingly
# while True:
#     # read data from serial and parse values
#     values = ser.readline().decode('utf-8').strip().split(',')
#     print(values)
#     # if len(values) != 3:
#     #     continue
#     nob1, nob2, nob3 = int(values[0]), int(values[1]), int(values[2])

#     # update master volume
#     # volume = asd(nob1, 0, 100, 0, 100)
#     # volume.SetMasterVolumeLevel(1.5, None)
