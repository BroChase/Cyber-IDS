from tkinter import*  # python3
from tkinter.ttk import Style, Frame
from fileHashEvent import *

from folderHasher import *
from tkinter import messagebox
from tkinter import filedialog
from networkEvent import *
import subprocess

HEADER_FONT = ("Helvetica", 36, "bold")
BODY_FONT = ("Helvetica", 20, "bold")
SMALL_FONT = ("Helvetica", 15)
BUTTON_FONT = ("Helvetica", 16, "bold")
D_GREY = "#767676"
L_GREY = "#aeaeae"

C_DGREY = "#767676"
C_LGREY = "#aeaeae"
C_SCREEN = "#C5C1C0"
C_STEEL = "#0A1612"
C_DENIM = "#1A2930"
C_MARIGOLD = "#F7CE3E"

DEST_IP = "192.168.10.2"
SRC_IP = "192.168.56.3"

class LearningApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("IDS/NIDS Learning Tool")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.resizable(width=False,height=False)

        #get screen dimensions and center window
        guiHeight = 800
        guiWidth = 1280
        xOffset = int(self.winfo_screenwidth()/2-guiWidth/2)
        yOffset = int(self.winfo_screenheight()/2-guiHeight/2)
        self.geometry("%dx%d+%d+%d" % (guiWidth, guiHeight, xOffset, yOffset))

        self.frames = {}
        for F in (WelcomePage, MainMenu, HIDS, NIDS):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        self.title(frame.title)

    def changeTitle(self, newTitle):
        self.title(newTitle)


class WelcomePage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        self.controller = controller
        WELCOME_FONT = ("Helvetica", 32, "bold")
        WELCOME_FONT2 = ("Helvetica", 16, "bold")

        self.title = "Welcome"
        photo = PhotoImage(file = "new_gui.pgm")
        background = Label(self, image=photo)
        background.image = photo
        background.place(x=0, y=0)

        #Title-Header
        lab_header = Label(self,text="Intrusion Detection System (IDS) Learning Tool", bg=C_SCREEN,fg=C_DENIM,font=HEADER_FONT)
        lab_header.pack(side=TOP, fill=X)

        #hack underline
        lab_underline =Label(self,bg="black")
        lab_underline.pack(side=TOP, fill=X)

        self.but_logView = Button(self, text="Launch log viewer", fg="black", bg=C_MARIGOLD, font=BODY_FONT,
                                  command=lambda: self.buttonclick(), relief=RAISED,bd=5)

        self.count = 0

        self.menutextindex = 0

        self.menutextlist = ["""Welcome to an Intrusion Detection System Learning Tool.""",
                             """This tool is to help teach you about Network-Based Intrusion Detection Systems (NIDS) and Host-Based Intrusion Detection Systems (HIDS)""",
                             """To show you how a HIDS and NIDS works, you will be walked through two modules in order to get a feel of how these systems work.""",
                             """It is important to note that an IDS only detects and alerts of suspicious activity, it does not prevent it or take action against it.\n\nFor that reason, most systems will write the events to a log that can be viewed by a user. """,
                             """To help display the functionality of the systems you will be using a log viewer that will display certain logged events detected by the HIDS and NIDS""",
                             """Please open the log viewer below and select which module you would like to launch first"""]


        self.mess_menu = Message(self, width=900,font=WELCOME_FONT, text=self.menutextlist[0], bd=10,
                                        background=C_DENIM, foreground="white", relief=RAISED, justify = CENTER, anchor=CENTER)

        #nav button placement frame
        navFrame = Frame(self)
        self.but_welcomeprevious = Button(navFrame,width=20,font=WELCOME_FONT2, text="<Prev", bg=C_MARIGOLD, fg="black", command=self.wPrevious, relief=RAISED,bd=5, state=DISABLED)
        self.but_welcomenext = Button(navFrame, width=20,font=WELCOME_FONT2, text="Next>", bg=C_MARIGOLD, fg="black", command=self.wNext, relief=RAISED,bd=5)

        self.mess_menu.place(anchor=CENTER,relx=.5,rely=.4)
        #self.mess_menu.pack(side=TOP, pady=(100,0))

        self.but_welcomeprevious.pack(side=LEFT)
        self.but_welcomenext.pack(side=RIGHT)
        navFrame.pack(side=BOTTOM, pady=(0,50))


    def wPrevious(self):
        self.but_welcomenext.config(state=NORMAL)
        self.but_logView.pack_forget()

        if self.menutextindex > 0:
            self.menutextindex -= 1
            self.mess_menu.config(text=self.menutextlist[self.menutextindex])

        if self.menutextindex == 0:
            self.but_welcomeprevious.config(state=DISABLED)

    def wNext(self):
        self.but_welcomeprevious.config(state=NORMAL)
        if self.menutextindex < len(self.menutextlist)-1:
            self.menutextindex += 1
            self.mess_menu.config(text=self.menutextlist[self.menutextindex])

        self.but_logView.pack_forget()
        if self.menutextindex == 5:
            self.but_logView.pack(side="bottom", pady=(0,50))
            self.but_welcomenext.config(state=DISABLED)

    def start(self):
        self.controller.show_frame("MainMenu")

    def launchLogviewer(self):
        subprocess.Popen("eventViewerMain.py", shell=True)

    def buttonclick(self):
        self.start()
        self.launchLogviewer()

class MainMenu(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.title = "Main Menu"

        #set photo background
        photo = PhotoImage(file = "new_gui.pgm")
        background = Label(self, image=photo)
        background.image = photo
        background.place(x=0,y=0)

        # lab_header = Label(self, text="Main Menu", background = D_GREY, foreground = "white", relief = RAISED, font = HEADER_FONT)
        # lab_header.pack(side="top", pady=10)
        #
        # lab_select = Label(self, text="Select a Simulation to Begin", background = D_GREY, foreground = "white", relief = RAISED, font = BODY_FONT)
        # lab_select.pack(side="top", pady=(0,70))

        #Title-Header
        lab_header = Label(self,text="Main Menu", bg=C_SCREEN,fg=C_DENIM,font=HEADER_FONT)
        lab_header.pack(side=TOP, fill=X)

        lab_header = Label(self,text="Select a Simulation to Begin", bg=C_SCREEN,fg=C_DENIM,font=BODY_FONT)
        lab_header.pack(side=TOP, fill=X)

        #hack underline
        lab_underline =Label(self,bg="black")
        lab_underline.pack(side=TOP, fill=X)

        but_sim1 = Button(self, text = "HIDS - Host-Based Intrusion Detection System", fg = "black", bg = C_MARIGOLD, font = BODY_FONT, command=lambda: controller.show_frame("HIDS"), wraplength=200,width=13, relief=RAISED,bd=10)
        but_sim1.place(relx=.375,rely=.5, anchor=CENTER)

        but_sim2 = Button(self, text = "NIDS - Network-Based Intrusion Detection System", fg = "black", bg = C_MARIGOLD, font = BODY_FONT, command=lambda: controller.show_frame("NIDS"), wraplength=200, width=13, relief=RAISED,bd=10)
        but_sim2.place(relx=.625,rely=.5, anchor=CENTER)

        but_logView=Button(self, text = "Re-open Log Viewer", fg = "black", bg = C_MARIGOLD, font = BUTTON_FONT, command=self.launchLogviewer, wraplength=200, width=15, relief=RAISED,bd=5)
        but_logView.place(relx=.5,rely=.85,anchor=CENTER)
        but_quit = Button(self, text="Quit", command=quit, font = BUTTON_FONT, bg = D_GREY, fg = "white")
        but_quit.pack(side = "bottom")

    def launchLogviewer(self):
        subprocess.Popen("eventViewerMain.py",shell=True)

class HIDS(Frame):
    """Made by Peter Gibbs 2016
    This is the lab for the host intrusion detection system, It allow the user to play with file hashing
    and show how an HIDS can use file hashing to find compromised files on a system"""
    def __init__(self, parent, controller):

        HIDSHEADER_FONT = ("Helvetica", 36, "bold")
        HIDSBODY_FONT = ("Helvetica", 20, "bold")
        HIDSSMALL_FONT = ("Helvetica", 13)
        HIDSBUTTON_FONT = ("Helvetica", 12, "bold")
        HIDSINFO_FONT=("Helvetica", 20, "bold")
        HIDS_BUTTON_WIDTH=30
        HIDS_BUTTON_HEIGHT=2
        Frame.__init__(self, parent)
        self.controller = controller
        self.folderPath="HIDS excercise"

        self.fileList=[]
        self.hashList=[]
        self.validList=[]
        self.listIndex=1

        self.invalidFileList={}#used to prevent duplicate events from being logged
        self.noDelayOnHash=False
        self.writeToLog=False
        self.tutorialTextIndex=0

        self.tutorialTextList=["""1: A HIDS is a software that get installed directly on the computer it is meant to monitor. This is different than a NIDS, which is typically placed outside of a network of computers.""",

        """1.1: A HIDS has the benefit of having access to the host’s files, which is why most HIDS monitor critical system files to ensure they haven’t been tampered with.""",

        """1.2: For this demonstration, we have selected a folder of various files that the HIDS will monitor. These files are shown above in the left-hand column.""",

        """1.3: To monitor the integrity of files, the HIDS must create a database of files in a known ‘good’ condition. The most efficient way to do this, is by storing a hash checksum of the file. If a single bit of the file is changed, it will have a completely different checksum.""",

        """2: Go ahead and click "Check Integrity of Files." You will notice in the middle column a list of cryptic letters and numbers. These are the individual MD5 checksums of the files.""",

        """2.1: You will also notice in the right column that every file says ‘false.’ This is because you haven’t yet created a database of ‘good’ hashes for the HIDS to compare against.""",

        """3: Let’s start by adding a single file to the ‘good’ database. Click the button “Add a Single File to Validation List” and choose any of the files.""",

        """3.1: Now click “Check Integrity of Files” again. You will notice that the file you selected is now considered valid.""",

        """3.2: By adding that single file to the good database, the HIDS now sees that file as valid because it hasn’t been changed.""",

        """3.3: Now click “Add all Files to Validation List” and then check their integrity. Ensure all files now say valid.""",

        """4: If you don’t have the log viewer open already, quit to the main menu and re-open the log viewer. Don’t worry, your progress will be saved. Return to this lab when you have opened the log viewer.""",

        """4.1: Now click the checkbox that says "Run Every 10 Seconds.” This essentially makes the HIDS run an integrity check on the files every 10 seconds. In a real HIDS you could set it up to run as often as you like.""",

        """4.2: Now open the folder in your operating system's file browser and edit some of the files.""",

        """4.3: If you look in the log viewer you should see that the files you changed have been logged as a critical alert.""",

        """5: Among many other things, a professional HIDS can be configured to perform many host-based checks such as making sure system logs aren't tampered with (usually a good sign of a hacker covering their tracks).""",

        """That concludes this lesson on Host-Based Intrusion Detection Systems. Feel free to play around with system as you wish. You can even select a new folder to monitor by clicking “Choose New Folder to Monitor.” Also, if you haven’t already, check out the Network Intrusion Detection System simulation."""]


        self.title = "Host-Based Intrusion Detection System (HIDS) Simulation"
        self.validationFilePath="validhashlist.txt"

        open(self.validationFilePath,'a').close()#if the logfile dosent exist then we make a new one
        #set photo background
        photo = PhotoImage(file = "new_gui.pgm")
        background = Label(self, image=photo)
        background.image = photo
        background.place(x=0,y=0)

        self.mess_infoAndHelp = Message(self, text=self.tutorialTextList[0],width=850, justify=LEFT, bd=10,
                                        background=C_DENIM, foreground="white", relief=RAISED, font=HIDSINFO_FONT)

        #Title-Header
        lab_header = Label(self,text="Host-Based Intrusion Detection System (HIDS)", bg=C_SCREEN,fg=C_DENIM,font=HEADER_FONT)
        lab_header.pack(side=TOP, fill=X)

        #hack underline
        lab_underline =Label(self,bg="black")
        lab_underline.pack(side=TOP, fill=X)


        self.fileNameListBox = Listbox(self, exportselection=0, height=18, font=HIDSSMALL_FONT)
        self.fileHashListBox = Listbox(self, exportselection=0, height=18, font=HIDSSMALL_FONT)
        self.fileValidListBox = Listbox(self, exportselection=0, height=18, font=HIDSSMALL_FONT)



        self.autoMode = IntVar()

        but_backToMain = Button(self,height=HIDS_BUTTON_HEIGHT,width=HIDS_BUTTON_WIDTH, text = "Exit to Main Menu", bg = C_MARIGOLD, fg = "black", font = HIDSBUTTON_FONT, command = lambda: controller.show_frame("MainMenu"))
        but_backToMain.pack(side=BOTTOM,anchor=W,padx=20,pady=(5,10))



        self.but_changeFolder=Button(self,height=HIDS_BUTTON_HEIGHT,width=HIDS_BUTTON_WIDTH, text = "Choose New Folder to Monitor", bg = C_MARIGOLD, fg = "black", font = HIDSBUTTON_FONT, command = self.setFolder)
        self.but_changeFolder.pack(side=BOTTOM,anchor=W,padx=20,pady=5)

        self.but_resetValidFileList=Button(self,height=HIDS_BUTTON_HEIGHT,width=HIDS_BUTTON_WIDTH, text = "Reset The Validation List", bg = C_MARIGOLD, fg = "black", font = HIDSBUTTON_FONT, command = self.resetValidationList)
        self.but_resetValidFileList.pack(side=BOTTOM,anchor=W,padx=20,pady=5)

        self.but_addAllToList = Button(self,height=HIDS_BUTTON_HEIGHT,width=HIDS_BUTTON_WIDTH, text="Add all Files to Validation List", bg=C_MARIGOLD, fg="black",font=HIDSBUTTON_FONT, command=self.addAllFilesToList)
        self.but_addAllToList.pack(side=BOTTOM,anchor=W,padx=20,pady=5)

        self.but_addFileToList=Button(self,height=HIDS_BUTTON_HEIGHT,width=HIDS_BUTTON_WIDTH, text = "Add Single File to Validation List", bg = C_MARIGOLD, fg = "black", font = HIDSBUTTON_FONT, command = self.addSingleFileToList)
        self.but_addFileToList.pack(side=BOTTOM,anchor=W,padx=20,pady=5)

        self.but_checkIntegrity=Button(self,height=HIDS_BUTTON_HEIGHT,width=HIDS_BUTTON_WIDTH, text = "Check Integrity of Files", bg = C_MARIGOLD, fg = "black", font = HIDSBUTTON_FONT, command = self.runLab)
        self.but_checkIntegrity.pack(side=BOTTOM,anchor=W,padx=20,pady=5)

        self.but_tutorialPrevious = Button(self,text="<Prev", bg=C_MARIGOLD, fg="black", font=HIDSBUTTON_FONT, state=DISABLED, command=self.tutPrevious)
        self.but_tutorialNext = Button(self, text="Next>", bg=C_MARIGOLD, fg="black", font=HIDSBUTTON_FONT, command=self.tutNext)


        ckbox_autoMode = Checkbutton(self, width=HIDS_BUTTON_WIDTH,
                                     text="Run Every 10 Seconds",
                                     variable=self.autoMode,
                                     command=self.setAutoMode)


        ckbox_autoMode.pack(side=BOTTOM, anchor=W, fill=X, padx=10, pady=(0,15))

        #self.mess_infoAndHelp.pack(side=BOTTOM, anchor=E,expand=YES,fill=BOTH)
        self.mess_infoAndHelp.place(relx=.98, rely=.771,width=900,height=200, anchor=E)

        #but_tutorialNext.pack(side=BOTTOM, anchor=S)
        #but_tutorialPrevious.pack(side=BOTTOM, anchor=S)
        self.but_tutorialNext.place(relx=0.7, rely=0.955, anchor=E, width=100)
        self.but_tutorialPrevious.place(relx=0.6, rely=0.955, anchor=E,width=100)

        self.fileNameListBox.pack(side=LEFT, fill=X, anchor=N,expand=YES,padx=(10,1), pady=(15,0))
        self.fileHashListBox.pack(side=LEFT, fill=X, anchor=N,expand=YES,padx=(1,1), pady=(15,0))
        self.fileValidListBox.pack(side=LEFT, fill=X, anchor=N,expand=YES,padx=(1,10), pady=(15,0))
        #self.fileValidList.pack(side=LEFT, fill=X, anchor=N, padx=1)

        #self.mess_infoAndHelp.pack(side=LEFT)



        #self.tutorialText.trace("w", self.tutPrevious)
        #self.tutorialText.trace("w", self.tutNext)
        self.folderPath = "HIDS excercise"
        self.folderHasher = FolderHasher(self.validationFilePath, self.folderPath)
        self.reloadFileNameList()




    def tutPrevious(self):
        self.but_tutorialNext.config(state=NORMAL)
        if self.tutorialTextIndex > 0:
            self.tutorialTextIndex-=1
        if self.tutorialTextIndex == 0:
            self.but_tutorialPrevious.config(state=DISABLED)
        #print(self.tutorialTextIndex)
        self.mess_infoAndHelp.config(text=self.tutorialTextList[self.tutorialTextIndex])
        self.changeButtonStates()


    def tutNext(self):
        self.but_tutorialPrevious.config(state=NORMAL)
        if self.tutorialTextIndex < len(self.tutorialTextList)-1:
            self.tutorialTextIndex+=1
        if self.tutorialTextIndex == len(self.tutorialTextList)-1:
            self.but_tutorialNext.config(state=DISABLED)
        self.mess_infoAndHelp.config(text=self.tutorialTextList[self.tutorialTextIndex])
        self.changeButtonStates()


    def changeButtonStates(self):
        #step 2 button config
        if self.tutorialTextIndex == 4:
            self.but_checkIntegrity.config(state=ACTIVE)
        #step 3
        elif self.tutorialTextIndex == 6:
            self.but_addFileToList.config(state=ACTIVE)
            self.but_checkIntegrity.config(state=NORMAL)
        #step 3.1
        elif self.tutorialTextIndex == 7:
            self.but_checkIntegrity.config(state=ACTIVE)
            self.but_addFileToList.config(state=NORMAL)
        #step 3.3
        elif self.tutorialTextIndex == 9:
            self.but_addAllToList.config(state=ACTIVE)
            self.but_checkIntegrity.config(state=ACTIVE)
        else:
            self.but_checkIntegrity.config(state=NORMAL)
            self.but_addFileToList.config(state=NORMAL)
            self.but_addAllToList.config(state=NORMAL)
            self.but_changeFolder.config(state=NORMAL)
            self.but_resetValidFileList.config(state=NORMAL)


    def addToInvalidList(self,fileName,fileHash):
        self.invalidFileList[fileName]=fileHash

    def checkIfOnInvalidList(self,_fileName,fileHash):
        return self.invalidFileList.get(_fileName)==fileHash

    def clearInValidFileList(self):
        self.invalidFileList={}

    def setAutoMode(self):
        #print("aaaa")
        if self.autoMode.get()==True:
            self.noDelayOnHash = True
            self.writeToLog=True

            self.runLab()
            self.after(10000, self.setAutoMode)
        else:
            self.noDelayOnHash=False
            self.writeToLog = False



    def runLab(self):
        if self.folderPath=="":
            self.selectFolderError()
        else:
            self.listIndex=1
            self.reloadFileNameList()
            self.runLabLoop()

    def runLabLoop(self):

        if self.listIndex<=len(self.fileList):
            name=self.fileList[self.listIndex-1]
            hash=self.hashList[self.listIndex-1]
            valid=self.validList[self.listIndex - 1]

            self.fileNameListBox.selection_clear(0,END)
            self.fileHashListBox.selection_clear(0, END)
            self.fileValidListBox.selection_clear(0,END)
            isValidString="False"
            if self.validList[self.listIndex-1]==1:
                isValidString="True"
            self.fileHashListBox.insert(END,self.hashList[self.listIndex-1])
            self.fileValidListBox.insert(END, isValidString)
            self.fileNameListBox.selection_set(self.listIndex,self.listIndex)
            self.fileHashListBox.selection_set(self.listIndex, self.listIndex)
            self.fileValidListBox.selection_set(self.listIndex, self.listIndex)
            self.fileValidListBox.see(self.listIndex)
            self.fileNameListBox.see(self.listIndex)
            self.fileHashListBox.see(self.listIndex)
            if self.validList[self.listIndex - 1] == 1:

                self.fileValidListBox.itemconfig(self.listIndex, {'fg': 'green'})

            else:
                if self.writeToLog==True:
                    if self.checkIfOnInvalidList(name,hash)==False:#if we havent already logged the bad file in this session,
                        #we log the bad file event by construction a fileHashEvent object
                        fileHashEvent(name,hash,False)

                        self.addToInvalidList(name,hash)#we add it to our local invalid file list so we dont constantly log hashEvents from the same bad file
                self.fileValidListBox.itemconfig(self.listIndex, {'fg': 'red'})
                #we then color the isValid value red to help the user notice the bad file

            self.listIndex+=1#increment the list index

            # the noDelay on hash is used if the user checks the "run every 10 seconds" box.
            #thatway when the user is playing in the folder changing files, they dont have to wait for the animation
            if self.noDelayOnHash==True:#
                self.after(1, self.runLabLoop)
            else:
                self.after(250, self.runLabLoop)#we wait a bit so the user can see us look at each file individuly

        else:
            #if we hit the end of our file list then we clear the highlight on the 3 listboxes
            self.fileNameListBox.selection_clear(0, END)
            self.fileHashListBox.selection_clear(0, END)
            self.fileValidListBox.selection_clear(0, END)


    def reloadFileNameList(self):
        #when the user selects a new folder, we clear all the lists and listboxes so we can write to them again
        self.fileList=[]
        self.hashList = []
        self.validList = []
        self.fileNameListBox.delete(0,END)
        self.fileHashListBox.delete(0, END)
        self.fileValidListBox.delete(0, END)
        self.fileNameListBox.insert(0,"File name")
        self.fileHashListBox.insert(0, "File Hash")
        self.fileValidListBox.insert(0, "IsValid")
        self.fileNameListBox.itemconfig(0,{'bg':'magenta'})
        self.fileHashListBox.itemconfig(0, {'bg':'magenta'})
        self.fileValidListBox.itemconfig(0, {'bg':'magenta'})
        #self.folderHasher=FolderHasher(self.folderPath)
        files=self.folderHasher.getFileNamesInFolder()
        self.fileList=files
        self.hashList=self.folderHasher.getHashesInFolder()
        self.validList=self.folderHasher.getValidationInFolder()
        #we write all the file names to the file name listbox
        for fileName in files:
            self.fileNameListBox.insert(END,fileName)








    def addSingleFileToList(self):
        options={}
        options['initialdir'] = os.getcwd()+'/'+self.folderPath


        file=filedialog.askopenfilename(**options)
        if file=="":
            self.invalidFileError()
            #self.addSingleFileToList()
        else:
            self.folderHasher.addSingleFileToValidHashList(file)

    def addAllFilesToList(self):
        self.clearInValidFileList()
        self.folderHasher.addFilesToValidHashList()


    def resetValidationList(self):
        self.clearInValidFileList()
        open(self.validationFilePath, 'w').close()

    def invalidFolderError(self):
        error=messagebox.showerror("INVALID FOLDER", "Please Select a valid folder")

    def invalidFileError(self):
        error=messagebox.showerror("INVALID File", "Please Select a valid file")

    def selectFolderError(self):
        error=messagebox.showerror("No folder selected", "Please select a folder first")

    def setFolder(self):
        options = {}
        options['initialdir'] = os.getcwd() + '/' + self.folderPath
        folder=filedialog.askdirectory(**options)

        if folder=="":
            self.invalidFolderError()
            #self.setFolder()
        else:
            #print(folder)
            self.folderPath = folder
            self.folderHasher=FolderHasher(self.validationFilePath,folder)
            self.reloadFileNameList()




class NIDS(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.title = "Network-Based Intrusion Detection System (NIDS) Simulation"
        self.count = 1

        #set photo background
        photo = PhotoImage(file = "new_gui.pgm")
        background = Label(self, image=photo)
        background.image = photo
        background.place(x=0,y=0)

        #Title-Header
        lab_header = Label(self,text="Network-Based Intrusion Detection System (NIDS)", bg=C_SCREEN,fg=C_DENIM,font=HEADER_FONT)
        lab_header.pack(side=TOP, fill=X)

        #hack underline
        lab_underline =Label(self,bg="black")
        lab_underline.pack(side=TOP, fill=X)

        self.msg_intro = Message(self, width = 1100, justify = CENTER, bd = 10,
                                 background = C_DENIM, foreground ="white", relief = RAISED, font = HEADER_FONT)
        #self.msg_intro.place(relx = .5, rely = .05, anchor = N)
        self.msg_intro.pack(side="top",pady=(250,0))

        but_backToMain = Button(self, text = "Exit to Main Menu", bg = C_MARIGOLD, fg ="black", font = BUTTON_FONT, command = self.backToMain, relief=RAISED,bd=5)
        but_backToMain.pack(side="bottom", pady=(10,0))

        #create navigation arrows
        arrow_container = Frame(self)
        arrow_container.pack(side="bottom")

        self.but_leftArrow = Button(arrow_container, text="<-Prev", bg=C_MARIGOLD, fg="black", font= BUTTON_FONT, command = self.back, relief=RAISED,bd=5, state=DISABLED)
        self.but_leftArrow.pack(side="left")

        self.but_rightArrow = Button(arrow_container, text="Next->",bg=C_MARIGOLD, fg="black", font= BUTTON_FONT, command = self.forward, relief=RAISED,bd=5)
        self.but_rightArrow.pack(side="right")

        self.but_portScan = Button(self, text="Scan Port", bg=C_MARIGOLD, font = BUTTON_FONT, command = lambda :self.scanPort(self.ent_portEntry.get()), relief=RAISED,bd=5)
        self.ent_portEntry = Entry(self, font = BODY_FONT, width = 10)

        self.lab_dosAttack = Label(self, width = 50, font = BODY_FONT)
        self.but_dosAttack = Button(self, text="Begin DoS Attack", font = BUTTON_FONT, bg = C_MARIGOLD, command = lambda :self.pingRequest(1), relief=RAISED,bd=5)

        self.intro()

    def back(self):
        if self.count > 1:
            self.count -= 1

        self.but_rightArrow.config(state=NORMAL)
        self.intro()

        if self.count == 1:
            self.but_leftArrow.config(state=DISABLED)

    def forward(self):
        self.but_leftArrow.config(state=NORMAL)
        if self.count < 11:
            self.count += 1

        if self.count == 11:
            self.but_rightArrow.config(state=DISABLED)
        self.intro()

    def intro(self):
        if self.count == 1:
            self.msg_intro.config(text = "A NIDS is a system that monitors network traffic and alerts a user if it "
                                        "detects malicious activity")
        elif self.count == 2:
            self.msg_intro.config(text="It does this by analyzing the packet sequences and comparing them against known signatures")
        elif self.count == 3:
            self.msg_intro.config(text="For this simulation, you will attempt to alert the NIDS by performing specific network attacks")
        elif self.count == 4:
            self.msg_intro.config(text="We will start by simulating a port scan. A NIDS can be set up to alert the user when it sees that ports are being scanned")
            self.but_portScan.pack_forget()
            self.ent_portEntry.pack_forget()
            self.msg_intro.pack_configure(pady=(200, 0))
        elif self.count == 5:
            self.msg_intro.config(text="Enter a port number (1-65535) to scan in the text box, and click 'Scan Port'\n Check the log after to see the result")
            self.msg_intro.pack_forget()
            self.msg_intro.pack(side="top", pady=(50,0))
            self.ent_portEntry.pack(side="top",pady=(200,0))
            self.but_portScan.pack(side = "top", pady=(10,0))
        elif self.count == 6:
            self.msg_intro.config(text="As you should have seen, the NIDS logged the event, giving information on the source and destination IP address, as well as the port number that was scanned")
            self.msg_intro.pack_configure(pady=(200, 0))
            self.but_portScan.pack_forget()
            self.ent_portEntry.pack_forget()
        elif self.count == 7:
            self.msg_intro.config(text="Another common network attack is a denial-of-service (DoS) attack. This is done by flooding the network with requests.")
            self.msg_intro.pack_configure(pady=(200, 0))
            self.but_dosAttack.pack_forget()
            self.lab_dosAttack.pack_forget()
        elif self.count == 8:
            self.msg_intro.config(text="We will show how the NIDS responds to a DoS attack by sending a ping request 1000 times. Click the button to start the request loop")
            self.msg_intro.pack_forget()
            self.msg_intro.pack(side="top", pady=(50,0))
            self.but_dosAttack.pack(side = "top", pady=(200,0))
            self.lab_dosAttack.pack(side="top",pady=(10,0))
        elif self.count == 9:
            self.msg_intro.config(text="As you should have seen in the log viewer, the NIDS created an alert because it saw the same request being repeated. \n\nIn reality, the NIDS would "
                                       "create the same alert for any packet sequence it saw repeated that many times")
            self.msg_intro.pack_configure(pady=(100, 0))
            self.but_dosAttack.pack_forget()
            self.lab_dosAttack.pack_forget()
        elif self.count == 10:
            self.msg_intro.pack_configure(pady=(100, 0))
            self.msg_intro.config(text="These slides showed only a few examples of what an NIDS might do. The rules can be set up to detect many other types of network attacks. \n\nThe important"
                                       " thing to remember is that a NIDS scans packet sequences and creates an alert if it sees something that could be dangerous.")
        elif self.count == 11:
            self.msg_intro.pack_configure(pady=(200, 0))
            self.msg_intro.config(text="This concludes the NIDS portion of this learning tool. Exit to the main menu and check out the HIDS simulation if you haven't already.")

    def scanPort(self, portNum):
        self.ent_portEntry.delete(0, 'end')

        if int(portNum) < 1 or int(portNum) > 65535:
            self.ent_portEntry.insert(0,"Invalid")
        else:
            self.ent_portEntry.insert(0,"Success")
            networkEvent(SRC_IP, DEST_IP,portNum,2,"Port Scan","The NIDS detected a port scan on port"+str(portNum))
        return

    def pingRequest(self, count):
        if count > 1000:
            networkEvent(SRC_IP,DEST_IP,1,3,"DoS Attack", "The source IP is attempting to flood the host network with pings")
            self.lab_dosAttack.config(text="DoS Ping Attack Complete: Check the Log")
            return
        newText = "Sending ping request " + str(count) + " to 192.168.10.2"
        self.lab_dosAttack.config(text=newText)
        self.after(5,lambda :self.pingRequest(count+1))

    def backToMain(self):
        self.count = 1
        self.ent_portEntry.pack_forget()
        self.but_portScan.pack_forget()
        self.but_dosAttack.pack_forget()
        self.lab_dosAttack.pack_forget()
        self.msg_intro.pack_configure(pady=(250, 0))
        self.intro()
        self.controller.show_frame("MainMenu")


if __name__ == "__main__":
    app = LearningApp()
    app.mainloop()