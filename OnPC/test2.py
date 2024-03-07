import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())

audino_ports = []
for p in ports:
    print(p)
    if "Arduino" in p.description:
        print("This is an Arduino!")
        port = p.device
