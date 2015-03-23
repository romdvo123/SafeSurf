import socket, getpass, time

BUFLEN = 1024

class Client:
    __init__(self,server="10.20.30.110",port=8082,timeout=3):
        self.soc = socket.socket()
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soc.connect((host,port))
        reply = ''
        ready = select.select([self.soc], [], [], timeout)
        if ready[0]:
            reply = soc.recv(BUFLEN)
        if not reply:
            print "Timeout"
        else:
            print reply

    def login(self):
        username = raw_input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        login_request = username + ";" + password
        self.soc.send(login_request)
        reply = soc.recv(BUFLEN).split(";")
        if len(reply) != 2:
            print "Error in reply"
        else:
            print reply[1]
            if reply[0] == "0":
                self.login()
            if reply[0] == "2":
                self.soc.close()
            if reply[0] == "1":
                self.directory()

    #def directory(self):
                    
            
            
        
