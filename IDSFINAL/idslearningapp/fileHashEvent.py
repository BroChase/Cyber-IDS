from eventSystem import event
class fileHashEvent(event):
    """hashing event that will log anything noteworthy from the hasher
    You can use this as a template for creating other events
    Example usage: invalidFileHashEvent("CoolFileName","SomeHash",False)
    when this is run it will create an event object with the file name, hash, and if it was valid, then write all the data to the log"""
    
    def __init__(self,fileName=None,fileHash=None,isValid=False):
        
        eventType="File Hash"
        description="This event is generated when the hasher scans a file, an invalid hash can be dangerous because if a file is changed then that means that an attacker could have inserted milicious code in the file"
        #we give our event a type, severity, and description then create our base event class with thease parameters
        
        event.__init__(self,eventType,3,description)


        #The following can be whatever you want, just be sure they can be encoded as a string in one form or another. Also provide documentation about each member
        self.fileName=fileName
        self.severity=1+(2*(isValid==False))
        self.fileHash=fileHash
        self.isValid=isValid
        self.writeToFile()#After setting our parameters the event should be automaticly logged to a file
