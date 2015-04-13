import socket, os, thread

BUFLEN = 1024

MSG_LOGIN_FAILED = "0;User login failed"
MSG_LOGIN_SUCCESS = "1;User login successful"
MSG_LOGIN_NOTRIES = "2;Exceeded login tries limit, closing connection"
MSG_WRONG_METHOD = "3;Wrong method name, available methods: "
MSG_USERNAME_EXISTS = "4;Username already in use, please try a different username"
MSG_SIGNUP_SUCCESS = "5;Signup successful! Closing connection"
BASE_PATH = os.getcwd()

class ConnectionHandler:
    def __init__(self,connection,address):
        print "Connected from: %s"%str(address)
        self.address = address
        self.client = connection
        self.path = BASE_PATH
        self.users = os.path.join(self.path,'users')
        self.methods = ('GET','ADD','REMOVE')
        self.client.send('OK')
        self.tries = 5
        self.user = None
        action = self.client.recv(BUFLEN)
        if action == 'LOGIN':
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
        elif action == 'SIGNUP':
            self.signup()
    def signup(self):
        signup_info = self.client.recv(BUFLEN)
        exists = False
        username,password,mac = signup_info.split(';')
        with open(self.users,'r') as users:
            users_list = users.read().split('\n')
            for user_info in users_list:
                user_info = user_info.split(';')
                if user_info[0] == username:
                    exists = True
                    break
            if exists:
                self.client.send(MSG_USERNAME_EXISTS)
                self.signup()
        if not exists:
            with open(self.users,'a') as users:
                signup_info = signup_info + ";%s"%self.address[0]
                users.write(signup_info + '\n')
                directory = os.path.join(BASE_PATH,"accounts",mac)
                os.makedirs(directory)
                self.client.send(MSG_SIGNUP_SUCCESS)
                self.client.close()
            
    def authentication(self):
        username,password = self.client.recv(BUFLEN).split(';')
        with open(self.users,'r') as users:
            users_list = users.read().split('\n')
            for user_info in users_list:
                user_info = user_info.split(';')
                if user_info[0] == username and user_info[1]== password:
                    self.user = user_info[2]
                    self.directory = os.path.join(BASE_PATH,self.user)
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
                elif self.request[0] == "ADD":
                    self.method_ADD()

    def method_GET(self):
        date = self.request[1]
        report = os.path.join(self.directory,date)
        if os.path.exists(report):
            with open(report,'r') as _report:
                report_info = _report.read()
                self.client.send(report_info)
        else:
            self.client.send("NOT FOUND")
            
def start_server(port=8082,handler=ConnectionHandler):
    soc = socket.socket(socket.AF_INET)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostbyname(socket.gethostname())
    soc.bind((host, port))
    print "Client server serving on %s:%d."%(host, port)#debug
    soc.listen(0)
    while 1:
        thread.start_new_thread(handler, soc.accept())

if __name__ == '__main__':
    start_server()
