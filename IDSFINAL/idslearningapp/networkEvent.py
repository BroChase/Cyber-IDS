from eventSystem import event
class networkEvent(event):
    def __init__(self,source_ip,dest_ip,portNum,severity,type,description):

        event.__init__(self,type,severity,description)
        self.source_ip=source_ip
        self.dest_ip=dest_ip
        self.portNum=portNum
        self.writeToFile()

#This is compatable with the file reader class I sent you, and should be compatable with the log viewer
#EXAMPLE USE:
#networkEvent("192.168.10.2","192.168.10.3","25565",2,"Port Scan","Port scans can be dangerous because an attacker can use them to find a way into a netowrk")
