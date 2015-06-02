import socket, getpass, time, os, time, hashlib

BUFLEN = 8192
DEFAULT_DIR = os.getcwd()

class Client:
    def __init__(self,host="10.20.30.150",port=8081):
        self.soc = socket.socket()
        self.soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        failed = False
        try:
            self.soc.connect((host,port))
        except:
            print "Could not connect to server, try to restart the program"
            failed = True
        if not failed:
            reply = ''
            self.methods = ('GET','ADD','REMOVE')
            self.blacklists = (('porn','domains','expressions','urls'),
                               ('ecommerce','domains','urls'),
                               ('countries','banned'))
            while 1:
                reply += self.soc.recv(BUFLEN)
                end = reply.find('OK')
                if end != -1:
                    break
            print reply
            self.soc.send('LOGIN')
    def login(self,username,password):
        password = hashlib.sha224(password).hexdigest()
        login_request = username + ";" + password
        self.soc.send(login_request)
        reply = self.soc.recv(BUFLEN).split(";")
        if len(reply) != 2:
            print "Error in reply"
        else:
            print reply[1]
            if reply[0] == "0":
                return reply[1]
            if reply[0] == "2":
                self.soc.close()
                return 'CLOSE'
            if reply[0] == "1":
                #self.requests()
                return 'OK'

    def directory(self,path):
        target_path = os.path.join(path,"Reports")
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        self.target_dir = target_path
        print "The reports will be saved in %s"%self.target_dir

    def requests(self):
        method_prompt = "Enter method:%s "%str(self.methods)
        method = raw_input(method_prompt)
        while method not in self.methods:
            print "Wrong method"
            method = raw_input(method_prompt)
        if method == 'GET':
            self.directory()
            self.method_GET(raw_input("Enter date(day-month-year): "))
        if method == 'ADD':
            self.method_ADD(raw_input("Enter blacklist%s: "
                                      %str([blacklist[0] for blacklist in self.blacklists])))
        if method == 'REMOVE':
            self.method_REMOVE(raw_input("Enter blacklist%s: "
                                      %str([blacklist[0] for blacklist in self.blacklists])))
        #add the other methods    
    
    def method_GET(self,date):
        if len(date.split("-"))<3:
            print "Date syntax error"
            return 'SYNTAX'
        self.soc.send('GET;' + date)
        report = self.soc.recv(BUFLEN)
        if report == 'NOT FOUND':
            print "Report from the date %s is missing"%date
            return 'NOT FOUND'
        else:
            with open(os.path.join(self.target_dir,date),'w') as new_report:
                new_report.write(report)
            info = "Wrote new report in %s for the date %s"% (self.target_dir,date)
            print info
            return info

    def method_ADD(self,blacklist,sub_blacklist,ban):
        self.soc.send('ADD;' + blacklist + ';' + sub_blacklist + ';' + ban)
        response = self.soc.recv(BUFLEN)
        if response == "SUCCESS":
            info = "Successfuly added %s to %s in blacklist %s"%(ban,sub_blacklist,blacklist)
            print info
            return info

    def method_REMOVE(self,blacklist,sub_blacklist,remove):
        self.soc.send('REMOVE;' + blacklist + ';' + sub_blacklist + ';' + remove)
        response = self.soc.recv(BUFLEN)
        if response == "SUCCESS":
            info = "Successfuly removed %s from %s in blacklist %s"%(remove,sub_blacklist,blacklist)
            print info
            return info
            
if __name__ == '__main__':
    c = Client()