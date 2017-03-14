from tkinter import*  # python3
from tkinter.ttk import *
from folderHasher import *
from tkinter import messagebox
from tkinter import filedialog
#import Tkinter as tk   # python

HEADER_FONT = ("Helvetica", 36, "bold")
BODY_FONT = ("Helvetica", 20, "bold")
SMALL_FONT = ("Helvetica", 15)
BUTTON_FONT = ("Helvetica", 16, "bold")
D_GREY = "#767676"
L_GREY = "#aeaeae"


class HIDS(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.folderPath=""
        self.title = "Host-Based Intrusion Detection System (HIDS) Simulation"
        #set photo background
        photo = PhotoImage(file = "new_gui.pgm")
        background = Label(self, image=photo)
        background.image = photo
        background.place(x=0,y=0)

        lab_header = Label(self, text = "Host-Based Intrusion Detection System (HIDS)", bg = D_GREY, fg = "white", font = BODY_FONT)
        lab_header.pack(pady=10)

        but_backToMain = Button(self, text = "Exit to Main Menu", bg = D_GREY, fg = "white", font = BUTTON_FONT, command = lambda: controller.show_frame("MainMenu"))
        but_backToMain.pack(side="bottom")

        #but_changeFolder=Button(self, text = "Chose folder to validate", bg = D_GREY, fg = "white", font = BUTTON_FONT, command = self.setFolder)
    #def invalidFileError(self):
        #error=messagebox.showerror("INVALID FOLDER", "Please Select a valid folder")

   # def setFolder(self):
       # self.folderPath= filedialog.askdirectory()
        #if self.folderPath=="":
            #self.invalidFileError()
            #self.setFolder(self)


       # print(os.path.getsize(self.logfile))