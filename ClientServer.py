import socket, os

BUFLEN = 1024

MSG_LOGIN_FAILED = "0;User login failed"
MSG_LOGIN_SUCCESS = "1;User login successful"
MSG_LOGIN_NOTRIES = "2;Exceeded login tries limit, closing connection"
MSG_WRONG_METHOD = "3;Wrong method name, available methods: "

class ConnectionHandler:
    def __init__(self,connection,address,base_path):
        print "Connected from: %s"%str(address)
        self.client = connection
        self.client.send("OK")
        self.path = base_path
        self.users = os.path.join(self.path,"users")
        self.methods = ("GET","ADD")
        self.tries = 5
        self.user = None
        for try_number in range(self.tries):
            if self.authentication() == 0:
                if try_number < self.tries - 1:
                    self.client.send(
                        MSG_LOGIN_FAILED +
                        "\nTry number: %d/%d"%(try_number+1,self.tries))
            else:
                break
        if self.user == None:
            self.client.send(MSG_LOGIN_NOTRIES)
        else:
            self.client.send(MSG_LOGIN_SUCCESS)
            self.handle_requests()
            
    def authentication(self):
        username,password = self.client.recv(BUFLEN).split(";")
        with open(self.users,'r') as users:
            users_list = users.split("\n")
            if [username,password] in [user_info.split()
                                       for user_info in users_list]:
                self.user = username
                return 1
        return 0
    
    def handle_requests(self):
        while 1:
            self.request = self.client.recv(BUFLEN).split()
            if self.request[0] not in self.methods:
                self.client.send(MSG_WRONG_METHOD + str(self.methods))
            else:

                if self.request[0] == "GET":
                    self.method_GET()
                else:
                    self.method_ADD()
                    
def start_server(base_path,host='localhost',
                 port=8082,handler=ConnectionHandler):
    soc = socket.socket(socket.AF_INET)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind((host, port))
    print "Client server serving on %s:%d."%(host, port)#debug
    soc.listen(0)
    while 1:
        thread.start_new_thread(handler, soc.accept()+(base_path,))
