from __future__ import print_function
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
    import serial
    import pystray
    from PIL import Image
    import os
    import subprocess
    import json
    import threading
    from threading import Event
    import serial.tools.list_ports
    import pythoncom
    import numpy as np

    def change_master_volume(volume_level):
        with open("minimum_value.txt", "r") as f:
            lowest_volume_limit = float(f.read())

        volume_level = asd(int(volume_level), 100, 0, lowest_volume_limit, 0)
        # print(volume_level)

        print(f"soejf h0ipw: {(np.emath.logn(1.07346, volume_level)) - 58.5582}")
        mate_idk = (np.emath.logn(1.07346, volume_level)) - 58.5582
        mate_idk = np.clip(mate_idk, lowest_volume_limit, 0)

        # print(f"Master volume raw: {mate_idk}")

        master_volume.SetMasterVolumeLevel(int(mate_idk), None)

    def change_volume(app, percentage):
        percentage = asd(int(percentage), 0, 100, 0, 1)
        print(app, percentage)
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name() == app:
                volume.SetMasterVolume(percentage, None)

    def getAudionoPort():
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print(p)
            if "USB Serial Port" in p.description:
                print("USB Serial Port")
                port = p.device
                break

        return port

    def getApps(slider):
        with open("C:/Users/Zippy/Documents/GitHub/Volume-controller/OnPC/flaskapp/sliders.json") as file:
            file = json.load(file)
            print(slider)
            print(file[0])
            print(file[1])
            print(file[2])
            print(file[3])
            apps = file[int(slider-2)]["apps"]
        
        return apps

    def open_action(icon, item):
        ui_exe_path = "C:/Windows/HelpPane.exe"
        subprocess.Popen(ui_exe_path)

    def quit_action(icon, item):
        event.set()
        icon.stop()
    
    def asd(num, in_min, in_max, out_min, out_max):
        return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    event = Event()

    image = Image.open("C:/Users/Zippy/Documents/GitHub/Volume-controller/OnPC/flaskapp/static/icon.png")

    icon = pystray.Icon(name='Volume Controller', icon=image, title='Volume controller')

    menu = (
        pystray.MenuItem('Open', open_action),
        pystray.MenuItem('Quit', quit_action),
    )

    # open serial port
    ser = serial.Serial(str(getAudionoPort()))
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    master_volume = cast(interface, POINTER(IAudioEndpointVolume))

    # print(ser.readline().decode('utf-8').strip())
    def read_serial_data(event: Event):
        pythoncom.CoInitialize()
        nob1_pre = int(ser.readline().decode('utf-8', 'ignore').strip().split(',')[0])
        nob1 = nob1_pre
        nob2_pre = int(ser.readline().decode('utf-8', 'ignore').strip().split(',')[1])
        nob2 = nob2_pre
        nob3_pre = int(ser.readline().decode('utf-8', 'ignore').strip().split(',')[2])
        nob3 = nob3_pre
        nob4_pre = int(ser.readline().decode('utf-8', 'ignore').strip().split(',')[3])
        nob4 = nob4_pre
        nob5_pre = int(ser.readline().decode('utf-8', 'ignore').strip().split(',')[4])
        nob5 = nob5_pre

        while True:
            if event.is_set():
                break

            if nob1 != nob1_pre:
                change_master_volume(int(nob1))
                nob1_pre = nob1

            if nob2 != nob2_pre and nob2 != nob2_pre+1 and nob2 != nob2_pre-1:
                nob2_pre = nob2
                apps = getApps(2)
                for app in apps:
                    change_volume(app, nob2)

            if nob3 != nob3_pre and nob3 != nob3_pre+1 and nob3 != nob3_pre-1:
                nob3_pre = nob3
                apps = getApps(3)
                for app in apps:
                    change_volume(app, nob3)

            if nob4 != nob4_pre and nob4 != nob4_pre+1 and nob4 != nob4_pre-1:
                nob4_pre = nob4
                apps = getApps(4)
                for app in apps:
                    change_volume(app, nob4)

            if nob5 != nob5_pre and nob5 != nob5_pre+1 and nob5 != nob5_pre-1:
                nob5_pre = nob5
                apps = getApps(5)
                for app in apps:
                    change_volume(app, nob5)
            

            nob1 = int(ser.readline().decode('utf-8', 'ignore').strip().split(',')[0])
            nob2 = int(ser.readline().decode('utf-8', 'ignore').strip().split(',')[1])
            nob3 = int(ser.readline().decode('utf-8', 'ignore').strip().split(',')[2])
            nob4 = int(ser.readline().decode('utf-8', 'ignore').strip().split(',')[3])
            nob5 = int(ser.readline().decode('utf-8', 'ignore').strip().split(',')[4])

            print(ser.readline().decode('utf-8', 'ignore').strip().split(','))

            

    # Start the thread
    threading.Thread(target=read_serial_data, args=(event,)).start()


    icon.menu = pystray.Menu(*menu)
    icon.on_click = open_action
    icon.run()

except Exception as e:
    print(f"error: {e}")
    input("CONTIENRIOKNAROIANSD PonaPOSIDNOIaSKN dPOKLNoiln;askd :OLNSADO:LKNAS:OD N:ALSDN:ONAS:OFINASODFNd O:AKLSDNL:KANSDO NAPSNDOANWD;oAIN WD;oAND:ON; OAWNDO :NAOFBoiaOIFB:OAIWBDo ;NAWD:O nAO:WIDN:oiBAWDOI bOFIABz")