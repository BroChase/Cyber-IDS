import os
import ast

class fileReader:
    def __init__(self,filepath):
        #object contains filepath when constructed
        #The object keeps a 'bookmark' of the end of the file when things are added to the file
        #it can continue from whare it left off

        #it also keeps track of the size of the file so it can check for changes without having to re read it
        self.filepath=filepath
        self.lastFileSize=0
        self.storedEventsSize=0

    def getfileSize(self):#gets the size of the file without reading it
        return os.path.getsize(self.filepath)

    def updateLastSize(self):#used in the read functions to let the object know that it dosent have to re read the file
        self.lastFileSize=self.getfileSize()

    def checkIfShouldRead(self):#if there are more events added to the file then this will return a True
        return self.lastFileSize<self.getfileSize()


    def readEntireFile(self):
        # not really used but if you want to read the entire file again without resetting the class members this should work
        #returns a list of dictionary objects, WILL ONLY IF THE FILE IS CREATED WITH THE EVENT CLASS OR A CHILD
        self.updateLastSize()
        output=[]
        with open(self.filepath,'r') as f:
            s=f.read().splitlines()
            for i in s:
                currentEvent=ast.literal_eval(i)
                output.append(currentEvent)
                self.storedEventsSize+=1
        f.close()

        return output



    def readUpdatedFile(self):
        #
        #returns a list of dictionary objects, WILL ONLY IF THE FILE IS CREATED WITH THE EVENT CLASS OR A CHILD
        self.updateLastSize()
        output=[]
        startingPoint=self.storedEventsSize


        with open(self.filepath,'r') as f:
            for i, line in enumerate(f):
                if i>=startingPoint:
                    currentEvent = ast.literal_eval(line)
                    output.append(currentEvent)
                    self.storedEventsSize += 1
            f.close()

        return output


