import socket, os, thread

BUFLEN = 1024

MSG_LOGIN_FAILED = "0;User login failed"
MSG_LOGIN_SUCCESS = "1;User login successful"
MSG_LOGIN_NOTRIES = "2;Exceeded login tries limit, closing connection"
MSG_WRONG_METHOD = "3;Wrong method name, available methods: "
MSG_USERNAME_EXISTS = "4;Username already in use, please try a different username"
MSG_SIGNUP_SUCCESS = "5;Signup successful! Closing connection"
MSG_MAC_EXISTS = "6;Computer is already registered. Closing connection"
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
        user_exists = False
        mac_exists = False
        username,password,mac = signup_info.split(';')
        with open(self.users,'r') as users:
            users_list = users.read().split('\n')
            for user_info in users_list:
                user_info = user_info.split(';')
                if len(user_info)==4:
                    if user_info[0] == username:
                        user_exists = True
                        break
                    if user_info[2] == mac:
                        mac_exists = True
            if user_exists:
                self.client.send(MSG_USERNAME_EXISTS)
                self.signup()
            if mac_exists:
                self.client.send(MSG_MAC_EXISTS)
                self.client.close()
        if not user_exists and not mac_exists:
            with open(self.users,'a') as users:
                signup_info = signup_info + ";%s\n"%self.address[0]
                users.write(signup_info)
                directory = os.path.join(BASE_PATH,'accounts',mac)
                if not os.path.exists(directory):
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
                    self.directory = os.path.join(BASE_PATH,'accounts',self.user)
                    print "Login successful from user %s with directory %s"%(self.user,
                                                                             self.directory)
                    return 1
        return 0
    
    def handle_requests(self):
        while 1:
            self.request = self.client.recv(BUFLEN).split(';')
            while len(self.request)<2:
                self.request = self.client.recv(BUFLEN).split(';')
            
            print self.request
            if self.request[0] not in self.methods:
                self.client.send(MSG_WRONG_METHOD + str(self.methods))
            else:
                if self.request[0] == 'GET':
                    date = self.request[1]
                    print "Getting report from date %s"%date
                    self.method_GET(date)
                elif self.request[0] == 'ADD':
                    blacklist,sub_blacklist,ban = self.request[1:]
                    print "Adding %s to %s in blacklist %s"%(ban,sub_blacklist,blacklist)
                    self.method_ADD(blacklist,sub_blacklist,ban)

    def method_GET(self,date):
        report = os.path.join(self.directory,date)
        print "Report path is %s"%report
        if os.path.exists(report):
            print report
            with open(report,'r') as _report:
                report_info = _report.read()
                print report_info
                self.client.send(report_info)
        else:
            self.client.send("NOT FOUND")
            self.handle_requests()

    def method_ADD(self,blacklist,sub_blacklist,ban):
        with open(os.path.join(BASE_PATH,'blacklists',blacklist,sub_blacklist),'a') as add_to:
            add_to.write(ban)
        self.client.send("SUCCESS")
        self.handle_requests()
        
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
