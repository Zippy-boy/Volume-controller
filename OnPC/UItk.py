import TKinterModernThemes as TKMT
from TKinterModernThemes.WidgetFrame import Widget
from tkinter import ttk

def buttonCMD():
        print("Button clicked!")

class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("TITLE", "Sun-valley", "dark")
        self.slider1_frame = ttk.Frame("Slider one")
        self.slider2_frame = ttk.Frame("Slider two")
        self.slider3_frame = ttk.Frame("Slider three")
        self.slider4_frame = ttk.Frame("Slider four")
        self.slider5_frame = ttk.Frame("Slider five")
        
        slider1 = ttk.Scale(from_=0, to=100, orient='vertical')
        slider2 = ttk.Scale(from_=0, to=100, orient='vertical')
        slider3 = ttk.Scale(from_=0, to=100, orient='vertical')
        slider4 = ttk.Scale(from_=0, to=100, orient='vertical')
        slider5 = ttk.Scale(from_=0, to=100, orient='vertical')

        self.slider1_frame.add(slider1)
        self.slider2_frame.add(slider2)
        self.slider3_frame.add(slider3)
        self.slider4_frame.add(slider4)
        self.slider5_frame.add(slider5)

        self.slider1_frame.grid(row=0, column=0)
        self.slider2_frame.grid(row=0, column=1)
        self.slider3_frame.grid(row=0, column=2)
        self.slider4_frame.grid(row=1, column=0)
        self.slider5_frame.grid(row=1, column=1)

       
        self.run()

App()