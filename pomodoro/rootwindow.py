import os
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from PIL import Image, ImageTk
from pomodoro.mainframe import MainFrame
from pomodoro.settingsframe import SettingFrame

class RootWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Pomodoro')
        self.geometry('250x250')
        self.resizable(False,False)        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.create_styling()
        self.create_frames()
        self.place_frames()

    @property
    def mainFrame(self):
        return self.__mainFrame

    @property
    def settingFrame(self):
        return self.__settingFrame
    
    def create_frames(self):
        self.__mainFrame = MainFrame(self)
        self.__settingFrame = SettingFrame(self)

    def place_frames(self):
        self.__mainFrame.grid(row=0, column=0,
                              sticky='NSEW')
        self.__settingFrame.grid(row=0, column=0, sticky='NSEW')
        self.__mainFrame.tkraise()

    def create_styling(self):
        self.style = Style()
        self.style.master = self
        self.style.theme_use('journal')
        self.style.configure("timeout.TLabel", foreground='red')        
        self.style.map(
            "pause.TButton",
            foreground=[('hover', self.style.lookup('TButton', 'background'))],
            background=[('hover', 'white')]
            )                
        
    def switch_frames(self, frame):
        frame.tkraise()

    def create_photo(self, w,h,file):
        with Image.open(os.path.join(os.path.dirname(__file__), f'src/{file}')) as image:
            photo = ImageTk.PhotoImage(
                image.resize((w, h), Image.ANTIALIAS))
            return photo

if __name__ == '__main__':
    rw = RootWindow()
    rw.mainloop()
