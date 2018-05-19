 
import liblo, time

class RemoteOSC():
    """ Using OSC to sync with a GUI """
    def __init__(self, port=8000):
        # send all messages to port 1234 on the local machine
        try:
            self.target = liblo.Address(port)
            self.active = True
        except liblo.AddressError as err:
            print("Error while opening OSC port " + str(port) + ": " + err)
            self.actie = False
    
    def launch(self, pattern, flag=True):
        """ signal on/off of a pattern """
        self.command("launch", pattern, flag)

    def record(self, pattern, flag=True):
        """ signal on/off of a record """
        self.command("record", pattern, flag)
        
    def through(self, pattern, flag=True):
        """ signal on/off of a midi through """
        self.command("through", pattern, flag)
        
    def command(self, address, pattern, flag):
        """ send lower level OSC command to GUI """
        msg = "/" + address + "_" + str(pattern)
        com = 1 if flag else 0
        print("Sending  value [" + str(com) + "] to " + msg)
        liblo.send(self.target, msg, com)

if __name__ == "__main__":
    print("Connect to OSC")
    remote = RemoteOSC()
    print("Launch patterns in turn")
    # plus one pattern to hacky turn off last one at the end
    for i in range(1,34):
        remote.launch(i)
        remote.record(i)
        remote.through(i)
        # switch off prevous
        if i > 0:
            remote.launch(i-1, False)
            remote.record(i-1, False)
            remote.through(i-1, False)
            time.sleep(0.1)
