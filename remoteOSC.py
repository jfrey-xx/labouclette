 
import liblo, time

class RemoteOSC(liblo.ServerThread):
    """ Using OSC to sync with a GUI """
    def __init__(self, client_port=8000, server_port=9000, server=False):
        """
        will send message to OSC instance on server_port of local machine, and listen to client_port
        NB: expect patterns indexed from 0 in input, output is indexed from 1
        """
        # init client
        print("Init client on localhost port " + str(client_port))
        try:
            self.target = liblo.Address(client_port)
            self.client_active = True
        except liblo.AddressError as err:
            print("Error while opening OSC port " + str(client_port) + ": " + err)
            self.client_active = False
    
        # init server if option set
        if server:
            print("Init server on localhost port " + str(server_port))
            try:
                liblo.ServerThread.__init__(self, server_port)
                self.start()
            except liblo.ServerError as err:
                print("Error while opening OSC port " + str(server_port) + ": " + err)
            
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
        """
        Send lower level OSC command to GUI
        pattern: number of the pattern, indexed from 0 (on server side it is indexed from 1)
        """
        if not self.client_active:
            print("Client not init, won't send OSC message.")
            return
        # fix index of pattern
        pattern += 1
        msg = "/" + address + "_" + str(pattern)
        com = 1 if flag else 0
        print("Sending  value [" + str(com) + "] to " + msg)
        liblo.send(self.target, msg, com)
        
    @liblo.make_method(None, None)
    def callback(self, path, args):
        """ a very generic callback when receive message, could be easier """
        # NB: on remote pattern indexed from 1
        print("received OSC message " + str(path) + " with data: " + str(args))
        
if __name__ == "__main__":
    print("Connect to OSC")
    remote = RemoteOSC(server=True)
    print("Launch patterns in turn")
    # plus one pattern to hacky turn off last one at the end
    for i in range(0,33):
        remote.launch(i)
        remote.record(i)
        remote.through(i)
        # switch off prevous
        if i > 0:
            remote.launch(i-1, False)
            remote.record(i-1, False)
            remote.through(i-1, False)
            time.sleep(0.1)

    input("press enter to quit...\n")