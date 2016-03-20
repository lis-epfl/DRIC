# -*- coding: utf-8 -*-
__doc__ = """
A simple chat example using a CherryPy webserver.

$ pip install cherrypy

Then run it as follow:

$ python app.py

You will want to edit this file to change the
ws_addr variable used by the websocket object to connect
to your endpoint. Probably using the actual IP
address of your machine.
"""
import random
import os

import cherrypy
import time

from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

cur_dir = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
index_path = os.path.join(cur_dir, 'index.html')
index_page = file(index_path, 'r').read()

class ChatWebSocketHandler(WebSocket):
    def received_message(self, m):
        print 'message sent by someone : ' + m.data
        cherrypy.engine.publish('websocket-broadcast', m)

    def closed(self, code, reason="A client left the room without a proper explanation."):
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))

class ChatWebApp(object):
    @cherrypy.expose
    def index(self):
        return index_page % {'username': "User%d" % random.randint(50, 1000),
                             # 'ws_addr': 'ws://localhost:9000/ws'}
                             'ws_addr': 'ws://' + getIpAdress() + ':9000/ws'}

    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

def publish_message(self, attr, m):
    t = time.localtime()
    msg = str(m)
    #print 'sent : ' + msg + 'at'
    cherrypy.engine.publish('websocket-broadcast', TextMessage(getTime()))

def getTime():
    from datetime import datetime

    dt = datetime.now()

    if dt.hour < 10:
        ret = ret + '0'
    ret = str(dt.hour) + 'h'

    if dt.minute < 10:
        ret = ret + '0'
    ret = ret + str(dt.minute) + 'min'

    if dt.second < 10:
        ret = ret + '0'
    ret = ret + str(dt.second) + "."

    if int(dt.microsecond/1000) < 10:
        ret = ret + '00'
    elif int(dt.microsecond/1000) < 100:
        ret = ret + '0'

    ret = ret + str(int(dt.microsecond / 1000))

    return ret

def getIpAdress():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    ip = s.getsockname()[0]
    s.close()
    return ip;

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 9000
    })
    
    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    import dronekit

    # LEquad must be launch for the folowing line
    vehicle = dronekit.connect("udp:localhost:14550")

    # add call back when receive an heartbeat
    vehicle.add_attribute_listener('last_heartbeat', publish_message)


    #cherrypy stuff
    cherrypy.config.update({'server.socket_host' : getIpAdress(),
                            'server.socket_port': 9000})

    conf = {
                '/': {
                    'tools.response_headers.on': True,
                    'tools.response_headers.headers': [
                        ('X-Frame-options', 'deny'),
                        ('X-XSS-Protection', '1; mode=block'),
                        ('X-Content-Type-Options', 'nosniff')
                    ]
                },
                '/ws': {
                    'tools.websocket.on': True,
                    'tools.websocket.handler_cls': ChatWebSocketHandler
                },
            }

    cherrypy.quickstart(ChatWebApp(), '', conf)
