### If you want to add more event types change this file. Be sure to document your changes and share this file with the group
#I have only added one derived class here as an example
import time

class event:
    """This is the base class for event"""
    def __init__(self,eventType,severity,description):
        """Apon creation of an event the time and date of the event are created automaticly
           Example usage found in hashFile event"""
        self.eventType=eventType
        self.severity=severity#Severity is on a 1-3 Scale with 1 being almost nothing and 5 being critical
        self.description=description
        self.time=time.strftime("%I:%M:%S")
        self.date=time.strftime("%d:%m:%Y")

    def writeToFile(self):
        """This should be called at the END of the constructor for any derived class. If it is not then the event created will not be recorded"""
        file=open("logfile.txt",'a')
        file.write(str(vars(self)))
        file.write('\n')
        file.close()
        



