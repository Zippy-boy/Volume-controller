from __future__ import print_function
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    import serial
    import pystray
    from PIL import Image
    import os
    import subprocess
    import json
    import serial.tools.list_ports

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
            apps = file[slider]["apps"]
        
        return apps

    def open_action(icon, item):
        ui_exe_path = "C:/Windows/HelpPane.exe"
        subprocess.Popen(ui_exe_path)

    def quit_action(icon, item):
        icon.stop()

    image = Image.open("C:/Users/Zippy/Documents/GitHub/Volume-controller/OnPC/flaskapp/static/icon.png")

    icon = pystray.Icon(name='Volume Controller', icon=image, title='Volume controller')

    menu = (
        pystray.MenuItem('Open', open_action),
        pystray.MenuItem('Quit', quit_action),
    )

    # open serial port
    ser = serial.Serial(str(getAudionoPort()))
    # print(ser.readline().decode('utf-8').strip())
    nob1_pre = ser.readline().decode('utf-8').strip().split(',')
    print(nob1_pre)


    icon.menu = pystray.Menu(*menu)
    icon.on_click = open_action
    icon.run()

except Exception as e:
    print(f"error: {e}")
    input("CONTIENRIOKNAROIANSD PonaPOSIDNOIaSKN dPOKLNoiln;askd :OLNSADO:LKNAS:OD N:ALSDN:ONAS:OFINASODFNd O:AKLSDNL:KANSDO NAPSNDOANWD;oAIN WD;oAND:ON; OAWNDO :NAOFBoiaOIFB:OAIWBDo ;NAWD:O nAO:WIDN:oiBAWDOI bOFIABz")