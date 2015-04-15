import socket, getpass, time, os, select

BUFLEN = 1024
DEFAULT_DIR = os.getcwd()
class Client:
    def __init__(self,host="10.20.30.102",port=8082,timeout=3):
        self.soc = socket.socket()
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soc.connect((host,port))
        reply = ''
        self.methods = ("GET","ADD","REMOVE")
        ready = select.select([self.soc], [], [], timeout)
        if ready[0]:
            reply = self.soc.recv(BUFLEN)
        if not reply:
            print "Timeout, closing connection"
            self.soc.close()
        else:
            print reply
            self.soc.send('LOGIN')
            self.login()

    def login(self):
        username = raw_input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        login_request = username + ";" + password
        self.soc.send(login_request)
        reply = self.soc.recv(BUFLEN).split(";")
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

    def directory(self):
        self.target_dir = raw_input("Enter directory(press enter for default): ")
        if not self.target_dir:
            self.target_dir = DEFAULT_DIR
        while not os.path.exists(self.target_dir):
            self.target_dir = raw_input("Directory doesn't exist, please try again(press enter for default): ")
            if not self.target_dir:
                self.target_dir = DEFAULT_DIR
        target_path = os.path.join(self.target_dir,"Reports")
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        self.target_dir = target_path
        print "The reports will be saved in %s"%self.target_dir
        self.requests()

    def requests(self):
        method = raw_input("Enter method: ")
        while method not in self.methods:
            print "Wrong method"
            method = raw_input("Enter method: ")
        if method == "GET":
            self.method_GET(raw_input("Enter date(day-month-year): "))
        #add the other methods    
    
    def method_GET(self,date):
        while len(date.split("-"))<3:
            print "Wrong date syntax"
            date = raw_input("Enter date(day-month-year): ")
        self.soc.send('GET ' + date)
        report = self.soc.recv(BUFLEN)
        if report == "NOT FOUND":
            print "Report from the date %s is missing"%date
        else:
            with open(os.path.join(self.target_dir,date),'w') as new_report:
                new_report.write(report)
            print "Wrote new report in %s for the date %s"% (self.target_dir,date)
            
if __name__ == '__main__':
    c = Client()
