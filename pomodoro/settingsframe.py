from tkinter import ttk
import tkinter as tk

class SettingFrame(ttk.Frame):

    def __init__(self, container):
        super().__init__(container)
        self.__container = container        
        self.columnconfigure((0,1,2),weight=1)        
        self.rowconfigure((0,5),weight=3)
        self.rowconfigure((1,2,3),weight=2)
        self.rowconfigure(4,weight=1)
        self.__newMappingHolder = {}
        self.__fromToMapping    = {0:[(25,59),(0,55)],
                                   1:[(0,5),(0,55)],
                                   2:[(6,19),(0,55)]}
        
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):                
        self.__settingPhoto = self.__container.create_photo(40, 40, 'settings.png')
        self.__title = ttk.Label(
            self,
            text='Welcome to Settings',
            image=self.__settingPhoto,
            compound = 'bottom',
            font='Arial 14 bold')
        for k,v in self.__container.mainFrame.pomodoroMapping.items():
            minHolder = tk.StringVar(self,value=int(v[0].split(':')[0]))     
            secHolder = tk.StringVar(self, value=int(v[0].split(':')[1]))            
            self.__newMappingHolder[k] = [minHolder,secHolder]       
            ttk.Label(
                self,
                text=f"{v[1]}:",style='primary.TLabel',
                font='SegoeUISymbol 12 bold', anchor='w'
                ).grid(row=k+1, column=0)
            ttk.Spinbox(
                self, from_=self.__fromToMapping[k][0][0],width=10,justify='center',
                to_=self.__fromToMapping[k][0][1],textvariable=minHolder,
                increment=1,state='readonly').grid(row=k+1, column=1)
            ttk.Spinbox(
                self, from_=self.__fromToMapping[k][1][0], width=10, justify='center',
                to_=self.__fromToMapping[k][1][1], textvariable=secHolder,
                increment=5, state='readonly').grid(row=k+1, column=2)
                                                
        self.__buttonFrame= ttk.Frame(self)
        self.__buttonFrame.columnconfigure((0,1),weight=1)        
        self.__buttonFrame.rowconfigure(0,weight=1)
        self.__confirmBtn= ttk.Button(
            self.__buttonFrame,
            style='pause.TButton',
            text='Confirm',
            width=10,
            command=self.confirm)
        self.__gobackBtn = ttk.Button(
            self.__buttonFrame,
            text='<- Go back',
            style='pause.TButton',
            width=10,
            command=self.go_back
            )

    def place_widgets(self):
        self.__title.grid(row=0,column=0,columnspan=3)
        self.__buttonFrame.grid(row=4,column=0,columnspan=3,sticky='EW',pady=(10,0))
        self.__gobackBtn.grid(row=0, column=1, sticky='W', padx=(3,0))
        self.__confirmBtn.grid(row=0, column=1, sticky='E',padx=(0, 13))

    def confirm(self):
        for k,v in self.__newMappingHolder.items():
            minute,second = int(v[0].get()),int(v[1].get())
            self.__container.mainFrame.pomodoroMapping[k][0] = f"{minute:02d}:{second:02d}"
        self.__container.mainFrame.buttonFrame.reset_timer()
                
    def go_back(self):
        self.__container.title('Pomodoro')
        self.__container.geometry('250x250')            
        self.__container.switch_frames(self.__container.mainFrame)