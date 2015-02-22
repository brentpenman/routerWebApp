import web
import socket

#set templates directory with html templates
render=web.template.render('/home/brent/bin/router/templates/')

#link urls to classes
urls = (
    '/', 'index'
)

#define router host and port
host = '192.168.2.214'
port = 5001
addr = (host,port)

#hexxer converts a decimal integer into a two character hex string
def hexxer(int):
    y = hex(int).split('x')[1]
    if len(str(y))==1:
	#in case it's a single digit string
	return '0'+str(y)
    else:
        return str(y)

def senddata(src,dst):
    #create the router check_sum data
    sum=src+dst+1
    #convert source, destination, and checksum ints into two character hex strings
    hexsum=hexxer(sum)
    hexsrc=hexxer(src)
    hexdst=hexxer(dst)
    #define a tcp socket
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #connect to socket on defined router    
    sock.connect((host,port))
    #create definition datagram data
    dataone = '1200'+hexsum+'000008'
    #create control datagram info
    datatwo = '00'+hexsrc+'00'+hexdst+'00000001'
    #send both datagrams as streams of hex
    sock.sendall(dataone.decode('hex'))
    sock.sendall(datatwo.decode('hex'))
    #close socket
    sock.close()


class index:
    def GET(self):
	#render /templates/index.html
	return render.index()
	
    def POST(self):
	#on a post, take the source and destination inputs
	route = web.input()
	source = route.get('source', None)
	dest = route.get('dest', None)
	print "sending source "+source+" to destination "+dest
	#send the command to the router
	senddata(int(source),int(dest))
	return "Sent Source "+source+" to Destination "+dest
	
#start the web server
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()