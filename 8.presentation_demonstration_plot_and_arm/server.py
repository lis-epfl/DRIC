
#   ### import ###

# system lib
import os
import os.path
import socket

# basic lib
import random
import string
import time
import threading
import numpy as np

# cherrypy lib
import cherrypy

# websocket communication lib
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage

# drone lib
import dronekit

#   ### global var ###

global IP_adr
# global vehicle
x = 0

# usefull function


def main():
    global vehicle
    IP_adr = getIpAdress()

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.config.update({'server.socket_host': IP_adr,
                            'server.socket_port': 8080})

    # for local simulated drone
    vehicle = dronekit.connect("udp:localhost:14550", rate=20)
    # vehicle = dronekit.connect('/dev/ttyUSB0', baud=57600, rate=20)
    print 'drone found, waiting ready'
    vehicle.wait_ready()
    # vehicle.parameters['COM_RC_IN_MODE'] = 2;

    vehicle.add_attribute_listener('armed', arm_callback)
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
    global x, vehicle
    x += 0.1

    # msg = str(2*np.sin(x))+';'+str(2*(np.sin(x+np.pi/2)))+';'+str(2*(np.sin(x+np.pi)))+';'+str(2*(np.sin(x+np.pi*3/2)))

    # trace format example :
    # plot:156.096;765.9866;739.0985;34.97
    #      trace1 ; trace2 ; trace3 ; trace4

    msg = 'plot:'
    msg += str(vehicle.attitude.pitch) + ';'
    msg += str(vehicle.attitude.roll) + ';'
    msg += str(vehicle.attitude.yaw)

    cherrypy.engine.publish('websocket-broadcast', msg)

    threading.Timer(0.080, publish_message).start()


def getIpAdress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip


def send_arm_state():
    global vehicle
    print 'sent arm state:' + str(vehicle.armed)
    if vehicle.armed:
        cherrypy.engine.publish('websocket-broadcast', TextMessage("server:state:arm"))
    else:
        cherrypy.engine.publish('websocket-broadcast', TextMessage("server:state:unarm"))


def arm_callback(self, attr, m):
    print 'arm_callback:' + str(m)
    send_arm_state()


#   ### classes definition ###


class WebSocketHandler(WebSocket):

    def received_message(self, m):
        print 'receive : ' + m.data
        global vehicle

        if m.data == "client:arm:switch":
            vehicle.commands.upload()

            isarmed = vehicle.armed

            # change vehicle arm state
            isarmed = not isarmed
            vehicle.armed = isarmed
            vehicle.commands.upload()

            # waiting during 5 seconds for chagement of arm state
            t1 = time.time()
            while vehicle.armed != isarmed and time.time() - t1 < 5:
                pass

            if vehicle.armed != isarmed:
                print 'error : cannot change arm state, timout after 5 seconds'

        elif m.data == "client:get:arm":
            send_arm_state()

    def closed(self, code, reason="A client left the room without a proper explanation."):
        print 'deconnexion of a client, reason :', reason


class Cherrypy_server(object):

    @cherrypy.expose
    def index(self):
        return file('public/html/index.html', 'r').read() % {'WS_ADR_GET': 'ws://' + getIpAdress() + ':8080/ws'}

    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))


if __name__ == '__main__':
    main()
