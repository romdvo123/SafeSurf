import socket, thread, select, FireWall, os


__version__ = '0.2.0 RomanProxy'
BUFLEN = 8192
VERSION = 'Python Proxy/'+__version__
HTTPVER = 'HTTP/1.1'
#BASE_PATH = r'W:\Cyber\romanproj\SafeSurf'
BASE_PATH = r'D:\Program Files (x86)\GitRepositories\SafeSurf'
bl_path = os.path.join(BASE_PATH,'blacklists')
geo_path = os.path.join(BASE_PATH,'GeoLiteCity.dat')
img_path = os.path.join(BASE_PATH,'response_picture.jpg')

firewall=FireWall.FireWall(bl_path,geo_path)
#WORKS, get new pic
with open(img_path,'rb') as image:
    data = image.read()
    MSG_PIC = HTTPVER+' 200 OK\n'+'Content-Type: image/jpeg\nContent-Length: '+str(len(data))+'\n\n' + data

MSG_CONTENT = HTTPVER+' 200 OK\n'+'Content-Type: text/html; charset=utf-8\n\n PROHIBITED CONTENT'
MSG_COUNTRY = HTTPVER+' 200 OK\n'+'Content-Type: text/html; charset=utf-8\n\n PROHIBITED HOST COUNTRY - '
class ConnectionHandler:
    def __init__(self, connection, address, timeout):
        self.client = connection
        self.client_buffer = ''
        self.timeout = timeout
        self.method, self.path, self.protocol = self.get_request_line()
        if firewall.blacklist_expressions_query(self.path) == 1:
            self.client.send(MSG_CONTENT)
            self.client.close()
        else:
            if self.method=='CONNECT':
                self.method_CONNECT()
            elif self.method in ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT',
                                 'DELETE', 'TRACE'):
                self.method_others()
            self.client.close()
            if self.target is not None:
                self.target.close()

    def get_request_line(self):
        while 1:
            self.client_buffer += self.client.recv(BUFLEN)
            end = self.client_buffer.find('\n')
            if end!=-1:
                break
        print '%s'%self.client_buffer[:end]#debug
        request_line = (self.client_buffer[:end+1]).split()
        self.client_buffer = self.client_buffer[end+1:]
        return request_line

    def method_CONNECT(self):
        self._connect_target(self.path)
        if self.target is not None:
            self.client.send(HTTPVER+' 200 Connection established\n'+
                             'Proxy-agent: %s\n\n'%VERSION)
            self.client_buffer = ''
            self._read_write()        

    def method_others(self):
        self.path = self.path[7:]
        if firewall.blacklist_url_query(self.path) == 1:
            self.client.send(MSG_CONTENT)
            self.client.close()
        else:
            i = self.path.find('/')
            host = self.path[:i]        
            path = self.path[i:]
            self._connect_target(host)
            if self.target is not None:
                self.target.send('%s %s %s\n'%(self.method, path, self.protocol)+
                                 self.client_buffer)
                self.client_buffer = ''
                self._read_write()

    def _connect_target(self, host):
        i = host.find(':')
        if i!=-1:
            port = int(host[i+1:])
            host = host[:i]
        else:
            port = 80
        if firewall.blacklist_domain_query(host) == 1:
            self.client.send(MSG_CONTENT)
            self.client.close()
            self.target = None
        else:
            try:
                (soc_family, _, _, _, address) = socket.getaddrinfo(host, port)[0]
                country = firewall.location_query(address[0])
                if country[0] == 1:
                    #_MSG_COUNTRY = MSG_COUNTRY + country[1]
                    #self.client.send(_MSG_COUNTRY)
                    self.client.send(MSG_PIC)
                    self.client.close()
                    self.target = None
                else:
                    self.target = socket.socket(soc_family)
                    self.target.connect(address)
            except socket.error:
                self.target = None
                print "UNKOWN ADDRESS"

        

    def _read_write(self):
        time_out_max = self.timeout/3
        socs = [self.client, self.target]
        count = 0
        while 1:
            count += 1
            (recv, _, error) = select.select(socs, [], socs, 3)
            if error:
                break
            if recv:
                for ready in recv:
                    data = ready.recv(BUFLEN)
                    if ready is self.client:
                        out = self.target
                    else:
                        out = self.client
                    if data:
                        out.send(data)
                        count = 0
            if count == time_out_max:
                break

def start_server(host='localhost', port=8081, IPv6=False, timeout=60,
                 handler=ConnectionHandler):
    if IPv6==True:
        soc_type=socket.AF_INET6
    else:
        soc_type=socket.AF_INET
    soc = socket.socket(soc_type)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind((host, port))
    print "Proxy server serving on %s:%d."%(host, port)#debug
    soc.listen(0)
    while 1:
        thread.start_new_thread(handler, soc.accept()+(timeout,))

if __name__ == '__main__':
    start_server()
