import os
from tkinter import *
from tkinter.ttk import *
#for some reason the import * is not working so we import some of the modules individually
from tkinter import messagebox
from tkinter import filedialog

from IDSFileReader import fileReader
dark_grey = "#767676"
light_grey = "#aeaeae"
class eventWindow(LabelFrame):



    """Log Viewer by Peter Gibbs 2016"""
    def __init__(self,parent):
        #self.LIST_HEIGHT=800
        LabelFrame.__init__(self,parent)
        #########################################################################################
        #Setting up the grid title
        #########################################################################################

        self.parent=parent#parent window
        self.logFile="logfile.txt"
        self.listOffset = 0  # Used to match the treeview to the list
        self.eventList=[]#events are logged as dictionarys and loaded into here
        self.fileReader=fileReader(self.logFile)#This opens our default logfile and reads it
        self.frame=Frame(parent)
        self.parent.option_add("*Font", "Arial 40 italic bold")#switch to a large font for the program title

        self.mess = Message(text="IDS LogViewer", width=700, justify=CENTER, bd=10,
                            background=dark_grey, foreground="white", relief=RAISED)#Large program title


        self.parent.option_add("*Font", "Arial 12")#switch back to a smaller font

        self.parent.columnconfigure(0, weight=1)#setup our tkinter grid
        self.frame.rowconfigure(2, weight=1)
        self.frame.pack(side=TOP, fill=BOTH, expand=Y)

        #########################################################################################
        # Setting up the table of events in the form of a treeview
        #########################################################################################

        self.columns = ('severity', 'type','date','time','info')

        self.treeview = Treeview(parent, columns=self.columns, show='headings')
        #########################################################################################
        # Setting up the other buttons and fetures
        #########################################################################################
        self.showColorsButtonVar=IntVar()#the show colors checkbox
        self.showColorsButtonVar.set(1)
        self.showColorsButton=Checkbutton(parent,text="Show Severity Colors",variable=self.showColorsButtonVar,
                                          command=self.setColor)

        self.autoReadFileButtonVar = IntVar()#The autorefresh varible
        self.autoReadFileButtonVar.set(1)
        self.refreshFileButton=Button(parent,text="Refresh",command=self.checkFile)#the refresh button

        self.clearLogButton = Button(parent, text="Clear Log",command=self.confirmClear)#the clear log button

        self.autoReadFileButton=Checkbutton(parent,text="Auto refresh",variable=self.autoReadFileButtonVar,
                                          command=self.checkFile)#the auto refresh checkbox

        self.eventInfoBox=Message(text="Click an event to view more information about it", width=550, justify=LEFT,anchor=N)#this displays more information about an event if the user clicks it
        self.initUI()#pack everything up
        self.setColor()
        self.checkFile()#load the file




        #########################################################################################
        # Setting up the menubar
        #########################################################################################

        menubar = Menu(parent)
        parent.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Change Logfile", command=self.setFile)
        menubar.add_cascade(label="File", menu=filemenu)

        filemenu.add_command(label="Exit", command=parent.quit)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=self.showAbout)
        helpmenu.add_command(label="How to use...", command=self.showHelp)
        menubar.add_cascade(label="Help", menu=helpmenu)


        #########################################################################################
        #Helper functions
        #########################################################################################
    def OnClick(self,event):
        #when the user double clicks an item in the list, display some more information about it

        curitem=str(self.treeview.focus())[1:]#we have to get the position of the object in the tree, Unfortunately
        #it is in a strangve hexadecimal form, I00A, or I015. We chop off the I because hex dosent even go to I
        #print(curitem)

        index=int(str(curitem),16)-1-self.listOffset#we then convert it to decimal, subtract one and subtract our list offset
        #Even when we clear the tree, any new events will still start off at the last items address +1 so we keep track of this
        #so we can still align the trees addresses with the index of out EventList
        #print(index)
        infoText=""

        curEvent=self.eventList[index]
        for keys in curEvent:
            infoText+=keys+": "+str(curEvent[keys])+'\n'+'\n'

        self.eventInfoBox.config(text=infoText)

    def clearLog(self):
        #clears the logfile and wipes the treeview
        open(self.logFile,'w').close()
        self.listOffset +=len(self.eventList)
        self.eventList=[]
        self.fileReader = fileReader(self.logFile)
        for i in self.treeview.get_children():
            self.treeview.delete(i)

    def confirmClear(self):
        if messagebox.askokcancel("LogViewer","WARNING:This will remove all events from the logfile you have loaded! Are you sure?"):
            self.clearLog()

    def showHelp(self):
        messagebox.showinfo("How to use...","""1. The program should load up a logfile apon startup if logfile.txt exists in the program folder already
        if not then you will have to load one in your self, click file->change logfile and browse to the file you want to load. The main ids is configured to write to a file called logfile.txt
         2. Once a file is loaded any events the IDS has recorded will show up on the main table, click the header of each column to sort by that catagory

         If you want to see color coded events then click the show colors checkbox

         If you want to clear the table then click clear log

         Double clicking an event will show all info associated with that event""")

    def showAbout(self):
        #called in the menubar, this displays the information about the program itself
        messagebox.showinfo("About This aplication", """This is the log viewing aplication for an IDS constructed as
        a project for an underguraduate course in cyber security.
        Made By Peter Gibbs, Joe Dodson
        and Chase Brown""")


    def setFile(self):
        #allows user to change logfile, apon changes clears the treeview and refreshes it
        self.logFile= filedialog.askopenfilename()

        self.eventList = []
        self.fileReader = fileReader(self.logFile)
        for i in self.treeview.get_children():
            self.treeview.delete(i)


        self.checkFile()

    def setColor(self):

        #When called, this function colors all the rows on the list acording to severity
        if self.showColorsButtonVar.get()==True:
            self.treeview.tag_configure('3 [Critical!]', background='red')
            self.treeview.tag_configure('2 [Moderate]', background='orange')
            self.treeview.tag_configure('1 [Low]', background='green')
        else:
            self.treeview.tag_configure('3 [Critical!]', background='white')
            self.treeview.tag_configure('2 [Moderate]', background='white')
            self.treeview.tag_configure('1 [Low]', background='white')



    def checkFile(self):
        #checks if any new events have been added, if so append them to the treeview
        if self.fileReader.checkIfShouldRead() == True:
            eventsToAdd=self.fileReader.readUpdatedFile()
            for i in eventsToAdd:
                self.insertEventToList(i)
                self.eventList.append(i)

        if self.autoReadFileButtonVar.get() == True:
            self.after(5000, self.checkFile)

    def insertEventToList(self,event):
        #the function that appends an event to the treeview
        #print(event['severity'])
        if event['severity']==3:
            Severity='3 [Critical!]'
        elif event['severity']==2:
            Severity = '2 [Moderate]'
        else:
            Severity = '1 [Low]'

        self.treeview.insert('', END, values=(Severity, event['eventType'], event['date'], event['time'], event['description']), tags=(Severity,))


    def initUI(self):
        #Moves all the elements into the window

        self.parent.title("Event Viewer")
        self.style = Style()
        self.style.theme_use("clam")

        self.mess.grid(in_=self.frame, row=0, column=0, sticky='nsew',columnspan=3, padx=5, pady=5)#add the title
        self.showColorsButton.grid(in_=self.frame, row=1, column=0, sticky='nsew', padx=5, pady=5)#add the color checkbox
        self.treeview.grid(in_=self.frame, row=2, column=0, sticky='nsew',columnspan=3, padx=5, pady=5)#add the treeview
        self.refreshFileButton.grid(in_=self.frame, row=1, column=2, sticky='nsew', padx=5, pady=5)#add the refresh button
        self.autoReadFileButton.grid(in_=self.frame, row=1, column=1, sticky='nsew', padx=5, pady=5)#add the autorefresh button
        self.clearLogButton.grid(in_=self.frame, row=1, column=3, sticky='nsew', padx=5, pady=5)#add the clearlog button
        self.eventInfoBox.grid(in_=self.frame, row=2, column=3, sticky='nsew', padx=5, pady=5)#add the information box
        #self.treeview.bind("<Double-1>", self.OnDoubleClick)#bind the double click on the treeview to the fuction that updates the messagebox
        self.treeview.bind("<<TreeviewSelect>>",self.OnClick)  # bind the double click on the treeview to the fuction that updates the messagebox

        #runs a sort on a column if the user clicks the heading of a column
        for col in self.columns:
            self.treeview.heading(col, text=col, command=lambda each_=col: self.treeview_sort_column(self.treeview,
                                                                                                     each_, False))



    #The sorting function
    def treeview_sort_column(self,tv, col, reverse):

        list = [(tv.set(k, col), k) for k in tv.get_children('')]#get all the events in given column in the treeview and add them to a list

        #sort the list
        list.sort(reverse=reverse)

        for index, (val, k) in enumerate(list):
            tv.move(k, '', index)#re arange the treeview to match the sorted list
           # self.eventList.remove(ind)
        #if the user clicks the column header again it reverses the elements from what they were before
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))


