import getpass, socket, select
from uuid import getnode as get_mac

BUFLEN = 1024
BANNED_CHAR = ';'

def signup(sock):
    username = raw_input("Enter username: ")
    while ';' in username:
        print "Usernames and passwords can't contain %s"%BANNED_CHAR
        username = raw_input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    while ';' in password:
        print "Usernames and passwords can't contain %s"%BANNED_CHAR
        password = raw_input("Enter password: ")

    password_repeat = getpass.getpass("Confirm password: ")
    while password != password_repeat:
        print "Password doesn't match"
        password_repeat = getpass.getpass("Confirm password: ")
    mac = get_mac()
    signup_request = username + ';' + password + ';' + str(mac)
    sock.send(signup_request)
    reply = sock.recv(BUFLEN).split(";")
    if len(reply) != 2:
        print "Error in reply"
    else:
        print reply[1]
        if reply[0] == '4':
            signup(sock)
        if reply[0] == '5' or reply[0] == '6':
            sock.close()

def start_connection(host="10.20.30.112",port=8081,timeout=3):
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
        ready = select.select([soc], [], [], timeout)
        while 1:
            reply += soc.recv(BUFLEN)
            end = reply.find('OK')
            if end != -1:
                break
        print reply
        soc.send('SIGNUP')
        signup(soc)

if __name__ == '__main__':
    start_connection()
