import os
import tkinter as tk
from tkinter import ttk
import threading
from playsound import playsound

class MainFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)        
        self.__container = container        
        self.rowconfigure((0, 2), weight=1)
        self.rowconfigure(1, weight=2)
        self.columnconfigure((0, 1), weight=1)
        
        self.__pomodoro = [0, 1, 0, 2]
        self.__pomodoroMapping = {0:['25:00','Pomodoro'],
                                  1: ['05:00', 'Short Break'],
                                  2:['15:00','Long Break']}
        self.__index = -1
        self.__currentStatus = None
        self.__timerStyle = True
        self.__backgroundPhoto = self.__container.create_photo(250,100,'frame.jpg')        
        self.create_widgets()
        self.place_widgets()
        self.rotate_status()

    @property
    def root(self):
        return self.__container

    @property
    def timeHolder(self):
        return self.__timeHolder

    @property
    def timerStyle(self):
        return self.__timerStyle
    
    @timerStyle.setter
    def timerStyle(self,newValue):
        self.__timerStyle = newValue
    
    @property
    def backgroundPhoto(self):
        return self.__backgroundPhoto
    
    def reset_index(self):
        self.__index = -1

    @property
    def pomodoroMapping(self):
        return self.__pomodoroMapping
    
    @property
    def buttonFrame(self):
        return self.__buttonFrame

    @property
    def timerLabel(self):
        return self.__timerLabel
    
    def create_widgets(self):
        self.__headerFrame = HeaderFrame(self)  
        self.__title = ttk.Label(self,
                                 font='Didot 19 bold',
                                 style='primary.TLabel')
        self.__timeHolder = tk.StringVar(self)
        self.__timerLabel = ttk.Label(
            self,            
            textvariable=self.__timeHolder,
            font = "Courier 24 bold"
            )
        self.__buttonFrame = ButtonFrame(self)

    def place_widgets(self):
        self.__headerFrame.grid(row=0, column=0, columnspan=2, sticky='NSEW')
        self.__title.grid(row=1, column=0)
        self.__timerLabel.grid(row=1, column=1)
        self.__buttonFrame.grid(row=2, column=0, columnspan=2, sticky='NSEW')

    def rotate_status(self):
        self.__index = (self.__index + 1) % len(self.__pomodoro)
        self.__timerLabel.config(style="TLabel")
        self.__timerStyle = True
        self.__currentStatus = self.__pomodoro[self.__index]
        self.__title.config(
            text=f'{self.__pomodoroMapping[self.__currentStatus][1]}')
        self.__timeHolder.set(
            value=self.__pomodoroMapping[self.__currentStatus][0])
    
class HeaderFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)        
        self.__container = container
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)                
        self.create_widgets()
        self.place_widgets()
    
    def create_widgets(self):            
        self.__label = ttk.Label(
            self,
            borderwidth=0,
            image=self.__container.backgroundPhoto)        
        self.__label.columnconfigure((0, 1, 2), weight=1)
        self.__label.rowconfigure(0, weight=1)
        self.__title = ttk.Label(
            self.__label,
            text='Pomodoro Timer !',
            font= "Arial 11 bold",
            background='#feb1bb',            
            foreground='white'            
            )            
        
        self.__settingPhoto = self.__container.root.create_photo(18, 18, 'settings.png')
        self.__settingBtn = ttk.Button(
            self.__label,
            text='Setting',
            width=6,
            image=self.__settingPhoto,
            compound='right',
            command=self.update_settings)

    def place_widgets(self):
        self.__label.grid(row=0,column=0,sticky='NSEW')                
        self.__title.grid(row=0, column=0,pady=(3,0),sticky='W')
        self.__settingBtn.grid(row=0, column=2)

    def update_settings(self):
        self.__container.root.title('Settings')
        self.__container.root.geometry('350x350')        
        self.__container.root.switch_frames(self.__container.root.settingFrame)

class ButtonFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        self.__container = container
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)     
        self.create_widgets()
        self.place_widgets()
        self.__id = None

    def create_widgets(self):
        self.__label = ttk.Label(
            self,
            borderwidth=0,
            image=self.__container.backgroundPhoto)
        self.__label.columnconfigure((0, 1, 2), weight=1)
        self.__label.rowconfigure(0, weight=1)        
        self.__startBtn = ttk.Button(
            self.__label, text='Start', width=6,
            command=self.start_timer)
        self.__pauseBtn = ttk.Button(
            self.__label, text='Pause', width=6, style='pause.TButton',
            command=self.pause_timer)
        self.__resetBtn = ttk.Button(
            self.__label, text='Reset', width=6,
            command=self.reset_timer)

    def place_widgets(self):
        self.__label.grid(row=0, column=0, sticky='NSEW')
        self.__startBtn.grid(row=0, column=0, sticky='E')
        self.__pauseBtn.grid(row=0, column=1)
        self.__resetBtn.grid(row=0, column=2, sticky='W')

    def start_timer(self):
        timer = self.__container.timeHolder
        minutes, seconds = map(lambda v: int(v), timer.get().split(':'))   
        total = minutes + seconds
        if total != 0:
            if seconds > 0:
                seconds -= 1
            else:
                seconds = 59
                minutes -= 1
            timer.set(value=f"{minutes:02d}:{seconds:02d}")            
            if  total < 11:
                if self.__container.timerStyle:
                    self.__container.timerLabel.config(style="timeout.TLabel")
                    self.__container.timerStyle = False     
                thread = threading.Thread(target=self.play_sound)   
                thread.start()                
            self.__id = self.after(999, self.start_timer)
        else:                        
            self.__container.rotate_status()
            self.__id = self.after(999, self.start_timer)

    def play_sound(self):
        playsound(os.path.join(os.path.dirname(__file__), r'src/countsound.wav'))
        
    def pause_timer(self):
        if self.__id:
            self.after_cancel(self.__id)

    def reset_timer(self):
        if self.__id:
            self.pause_timer()
        self.__container.reset_index()
        self.__container.rotate_status()