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

sampling_data = 0

class ChatWebSocketHandler(WebSocket):
    def received_message(self, m): #when a message is sent by the client
        print 'receive : ' + m.data

        if m.data == "client:arm:switch":
            wait_for_new_heartbeat(vehicle)

            isarmed = vehicle.armed

            # change vehicle arm state
            isarmed = not isarmed
            vehicle.armed = isarmed
            wait_for_new_heartbeat(vehicle)

            # check if state has changed
            new_isarmed = vehicle.armed

            if new_isarmed != isarmed:
                print 'error : cannot change arm state'

            # arm state is automatically sent by an arm call_back         


        elif m.data == "client:get:arm":
            send_arm_state()

        elif m.data == "client:state:arm":
            if vehicle.armed == False: 
                send_arm_state() #rectification of the client state

        elif m.data == "client:state:unarm":
            if vehicle.armed == True:
                send_arm_state() #rectification of the client state

    def closed(self, code, reason="A client left the room without a proper explanation."): #when someone close the connection
        print('websocket-broadcast', TextMessage(reason))
        # nothing else

class ChatWebApp(object):
    @cherrypy.expose
    def index(self): # configuration
        return index_page % {'username': "User%d" % random.randint(50, 1000),
                             # 'ws_addr': 'ws://localhost:9000/ws'}
                             'ws_addr': 'ws://' + getIpAdress() + ':9000/ws'}

    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))


def publish_message(self, attr, m): #send a message
    cherrypy.engine.publish('websocket-broadcast', TextMessage(msg))


def send_arm_state():
    print 'sent arm state:' + str(vehicle.armed)
    if vehicle.armed:
        cherrypy.engine.publish('websocket-broadcast', TextMessage("server:state:arm"))
    else:
        cherrypy.engine.publish('websocket-broadcast', TextMessage("server:state:unarm"))

def wait_for_new_heartbeat(my_vehicle):
    the_time = 0
    while my_vehicle.last_heartbeat >= the_time :
        the_time = my_vehicle.last_heartbeat


def arm_callback(self, attr, m):
    # print 'arm_callback:' + str(m)
    send_arm_state()

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
    # vehicle.add_attribute_listener('last_heartbeat', publish_message)
    vehicle.add_attribute_listener('armed', arm_callback)

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


# possible message :
# s->c means : 'message sent by the server to the client' (and oposite for c->s)

# 1. if s->c "server:state:arm"       send info        : for server, drone is armed
# 2. if s->c "server:state:unarm"     send info        : or server, drone is not armed
# 3. if s->c "server:get:arm"         request info     : want to know if arm or not (in the point of view from the client), expecting answer type 6 or 7

# 4. if c->s "client:arm:switch"      order            : client want to switch arm status, expect answer type 1 or 2
# 5. if c->s "client:get:arm"         request info     : want to know if arm or not, expecting answer type 1 or 2
# 6. if c->s "client:state:arm"       send info        : for client, drone is armed
# 7. if c->s "client:state:unarm"     send info        : for client, drone is not armed
# 
# TODO : error code
