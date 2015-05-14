import socket, getpass, time, os, select, time

BUFLEN = 8192
DEFAULT_DIR = os.getcwd()

class Client:
    def __init__(self,host="10.0.0.3",port=8081,timeout=3):
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
            self.login()
    def login(self):
        '''username = raw_input("Enter username: ")
        password = getpass.getpass("Enter password: ")'''
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
                self.requests()

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
        while len(date.split("-"))<3:
            print "Wrong date syntax"
            date = raw_input("Enter date(day-month-year): ")
        self.soc.send('GET;' + date)
        report = self.soc.recv(BUFLEN)
        if report == "NOT FOUND":
            print "Report from the date %s is missing"%date
        else:
            with open(os.path.join(self.target_dir,date),'w') as new_report:
                new_report.write(report)
            print "Wrote new report in %s for the date %s"% (self.target_dir,date)
        self.requests()

    def method_ADD(self,blacklist):
        exists = False
        while not exists:
            for _blacklist in self.blacklists:
                if _blacklist[0] == blacklist:
                    exists = True
                    bl =_blacklist[1:]
                    break
            if exists:
                break
            print "Wrong blacklist"
            blacklist = raw_input("Enter blacklist%s: "%str([blacklist[0] for blacklist in self.blacklists]))
        sub_blacklist = raw_input("Enter sub-blacklist%s: "%str([sub_bl for sub_bl in bl]))
        while sub_blacklist not in bl:
            print "Wrong sub-blacklist"
            sub_blacklist = raw_input("Enter sub-blacklist%s: "%str([sub_bl for sub_bl in bl]))
        ban = raw_input("Enter parameter to ban: ")
        self.soc.send('ADD;' + blacklist + ';' + sub_blacklist + ';' + ban)
        response = self.soc.recv(BUFLEN)
        if response == "SUCCESS":
            print "Successfuly added %s to %s in blacklist %s"%(ban,sub_blacklist,blacklist)
        self.requests()

    def method_REMOVE(self,blacklist):
        exists = False
        while not exists:
            for _blacklist in self.blacklists:
                if _blacklist[0] == blacklist:
                    exists = True
                    bl =_blacklist[1:]
                    break
            if exists:
                break
            print "Wrong blacklist"
            blacklist = raw_input("Enter blacklist%s: "%str([blacklist[0] for blacklist in self.blacklists]))
        sub_blacklist = raw_input("Enter sub-blacklist%s: "%str([sub_bl for sub_bl in bl]))
        while sub_blacklist not in bl:
            print "Wrong sub-blacklist"
            sub_blacklist = raw_input("Enter sub-blacklist%s: "%str([sub_bl for sub_bl in bl]))
        remove = raw_input("Enter parameter to remove: ")
        self.soc.send('REMOVE;' + blacklist + ';' + sub_blacklist + ';' + remove)
        response = self.soc.recv(BUFLEN)
        if response == "SUCCESS":
            print "Successfuly removed %s from %s in blacklist %s"%(remove,sub_blacklist,blacklist)
        self.requests()
            
if __name__ == '__main__':
    c = Client()
