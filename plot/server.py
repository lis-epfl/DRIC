
    ### import ###

# system lib
import os, os.path
import socket

# basic lib
import random
import string
import time, threading
import numpy as np

# cherrypy lib
import cherrypy

# websocket communication lib
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

# drone lib
import dronekit


    ### global var ###

global IP_adr
x = 0


    ### usefull function

def main():
    IP_adr = getIpAdress() 

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.config.update({'server.socket_host' : IP_adr,
                            'server.socket_port': 8080})

    publish_message()

    conf = {
        '/': 
        {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },

        '/ws': 
        {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': WebSocketHandler
        },

        '/static': 
        {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.quickstart(Cherrypy_server(), '/', conf)

def publish_message():
    global x
    x += 0.1

    msg = '1:'+str(2*np.sin(x))+';2:'+str(2*(np.sin(x+np.pi/2)))+';3:'+str(2*(np.sin(x+np.pi)))+';4:'+str(2*(np.sin(x+np.pi*3/2)))
    cherrypy.engine.publish('websocket-broadcast', msg)

    threading.Timer(0.100, publish_message).start()

def getIpAdress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    ip = s.getsockname()[0]
    s.close()

    return ip;


    ### classes definition ###

class WebSocketHandler(WebSocket):
    def received_message(self, m):
        print 'message sent by someone : ' + m.data
        cherrypy.engine.publish('websocket-broadcast', m)

    def closed(self, code, reason="A client left the room without a proper explanation."):
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))


class Cherrypy_server(object):
    @cherrypy.expose
    def index(self):
        return file('public/html/index.html', 'r').read() % {'WS_ADR_GET': 'ws://' + getIpAdress() + ':8080/ws'}

    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))


if __name__ == '__main__':
    main()