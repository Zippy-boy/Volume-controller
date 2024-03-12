from __future__ import print_function
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    import serial


    def change_master_volume(volume):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        master_volume = cast(interface, POINTER(IAudioEndpointVolume))
        master_volume.SetMasterVolumeLevel(volume, None)


    # open serial port
    ser = serial.Serial('COM4')
    print(ser.readline().decode('utf-8').strip())
    nob1_pre = int(ser.readline().decode('utf-8').strip().split(',')[0])

    while True:
        values = ser.readline().decode('utf-8').strip().split(',')
        print(values)
        if len(values) != 3:
            continue
        nob1 = int(values[0])

        if nob1 != nob1_pre:
            if nob1 + 1 != nob1_pre and nob1 - 1 != nob1_pre:
                print("Main Volume: " + str(nob1))
                volume_level = nob1 / 100 * -37  # Map nob1 value to the desired volume range
                change_master_volume(int(volume_level))
                nob1_pre = nob1

except Exception as e:
    print(e)
    input("Press Enter to continue...")
