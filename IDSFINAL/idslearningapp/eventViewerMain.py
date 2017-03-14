


from eventViewerWindow import*
#This is the main driver file for the event viewer
def main():
    file = open("logfile.txt", 'a').close()#create a logfile if none exists
    root = Tk()#setup our tkinter window
    root.geometry("1600x800")

    root.config(background=dark_grey)


    app = eventWindow(root)#construct our log viewer
    root.mainloop()

if __name__ == '__main__':
    main()#run it