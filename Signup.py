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
        if reply[0] == '5':
            sock.close()

def start_connection(host="10.0.0.3",port=8082,timeout=3):
    soc = socket.socket()
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.connect((host,port))
    reply = ''
    ready = select.select([soc], [], [], timeout)
    if ready[0]:
        reply = soc.recv(BUFLEN)
    if not reply:
        print "Timeout, closing connection"
        soc.close()
    else:
        print reply
        soc.send('SIGNUP')
        signup(soc)

if __name__ == '__main__':
    start_connection()
