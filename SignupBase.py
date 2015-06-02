import getpass, socket, select, hashlib
from uuid import getnode as get_mac

BUFLEN = 1024
class Client:
    def __init__(self,host="10.20.30.114",port=8081):
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
            self.connected = True
            while 1:
                reply += self.soc.recv(BUFLEN)
                end = reply.find('OK')
                if end != -1:
                    break
            print reply
            self.soc.send('SIGNUP')

    def signup(self,username,password,confirm):
        if ';' in username or ';' in password:
            print "Usernames and passwords cannot contain ;"
            return 'CHAR'
        if password != confirm:
            print "Passwords don't match"
            return 'NO MATCH'
        password = hashlib.sha224(password).hexdigest()
        mac = get_mac()
        signup_request = username + ';' + password + ';' + str(mac)
        self.soc.send(signup_request)
        reply = self.soc.recv(BUFLEN).split(";")
        if len(reply) != 2:
            print "Error in reply"
            return 'ERROR'
        else:
            print reply[1]
            if reply[0] == '4':
                return 'USERNAME'
            elif reply[0] == '6':
                self.soc.close()
                return 'REGISTERED'
            elif reply[0] == '5':
                self.soc.close()
                return 'SUCCESS'

'''def start_connection(host="10.0.0.2",port=8081,timeout=3):
    soc = socket.socket()
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    failed = False
    try:
        soc.connect((host,port))
    except:
        print "Could not connect to server, try to restart the program"
        failed = True
    if not failed:
        reply = ''
        while 1:
            reply += soc.recv(BUFLEN)
            end = reply.find('OK')
            if end != -1:
                break
        print reply
        soc.send('SIGNUP')
        signup(soc)'''

'''if __name__ == '__main__':
    c=Client()'''
