from __future__ import print_function
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
    import serial
    import math
    import time


    def change_per(app, percentage):
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name() == app:
                volume.SetMasterVolume(percentage, None)


    # activate the master volume control interface
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    master_volume = cast(interface, POINTER(IAudioEndpointVolume))

    # get all audio sessions
    sessions = AudioUtilities.GetAllSessions()


    def asd(num, in_min, in_max, out_min, out_max):
        return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


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

    # find the Discord session
    discord_session = None
    for session in sessions:
        try:
            if session.Process and session.Process.name() == 'Discord.exe':
                discord_session = session
                break
        except:
            pass

    # activate the Discord volume control interface
    if discord_session is not None:
        discord_volume = discord_session._ctl.QueryInterface(ISimpleAudioVolume)

    # open serial port
    ser = serial.Serial('COM4')
    values = ser.readline().decode('utf-8').strip().split(',')
    nob1_pre, nob2_pre, nob3_pre = int(values[0]), int(values[1]), int(values[2])



    # read data from serial and update volumes accordingly
    while True:
        # read data from serial and parse values
        values = ser.readline().decode('utf-8').strip().split(',')
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

        # update spotify volume
        if nob2 != nob2_pre:
            if nob2+1 != nob2_pre and nob2-1 != nob2_pre:
                print("Spotify: " + str(nob2))
                spotify_volume_level = asd(nob2, 0, 100, 0, 1)
                change_per("Spotify.exe", spotify_volume_level)
                nob2_pre = nob2

        # update discord volume
        if nob3 != nob3_pre:
            if nob3+1 != nob3_pre and nob3-1 != nob3_pre:
                print("discord: " + str(nob3))
                discord_volume_level = asd(nob3, 0, 100, 0, 1)
                change_per("Discord.exe", discord_volume_level)
                nob3_pre = nob3

        # time.sleep(0.01)

except Exception as e:
    print(e)
    input("Press Enter to continue...")