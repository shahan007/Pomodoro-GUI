import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
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
        self.style.configure("extreme.TFrame",background='black')
        self.style.map("pause.TButton",
                       foreground=[('hover', 'red')],
                       background=[('hover', 'white')])
        
    def switch_frames(self, frame):
        frame.tkraise()

if __name__ == '__main__':
    rw = RootWindow()
    rw.mainloop()
