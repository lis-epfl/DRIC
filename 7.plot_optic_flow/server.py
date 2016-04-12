
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

# plot libs
import json
import plotly

#   ### global var ###

global IP_adr
global vehicle
x = 0

can = np.array([0.0])
cad = np.array([0.0])
def handle_can(self, name, msg):
    '''
    Handle debug vects sent by saccade_telemetry
    '''
    if msg.name == 'CAN and CA':
        can[0] = msg.x
        cad[0] = msg.y
        # print cad


of_loc = np.array([-160.875 + 1.125 * i for i in range(125)]
                + [  19.125 + 1.125 * i for i in range(125)]
                + [  159.75 + 1.125 * i for i in range(50) ])
of     = np.zeros(300)
def handle_of(self, name, msg):
    '''
    Handle messages of type 'BIG_DEBUG_VECT'
    '''
    id, step = msg.name.split('_')
    if id == 'OF':
        step = int(step)
        i = 60 * step
        j = 60 * (step + 1)
        of[i:j] = msg.data

        # if step == 4:
            # print(of)
        #     publish_message(self)

def main():
    # IP_adr = getIpAdress()
    IP_adr = '0.0.0.0'

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.config.update({'server.socket_host': IP_adr,
                            'server.socket_port': 8080})

    # Use mavric message set
    dronekit.mavutil.set_dialect('mavric')

    # Create vehicle
    # vehicle = dronekit.connect("udp:localhost:14550", rate=100)
    vehicle = dronekit.connect('/dev/ttyUSB0', baud=57600, rate=500)

    # Add custom message callbacks
    vehicle.add_message_listener('BIG_DEBUG_VECT', handle_of)
    vehicle.add_message_listener('DEBUG_VECT', handle_can)

    # vehicle.parameters['COM_RC_IN_MODE'] = 2;

    publish_message(vehicle)

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


def publish_message(vehicle):

    # print(cad2)

    msg = {
        'data': [{
                    't': [np.rad2deg(cad[0]), np.rad2deg(cad[0])],
                    'r': [0, 1000],
                    'type': 'bar',
                    # 'mode': 'lines+markers',
                    # 'line': {'witdh': 10},
                    'name': 'CAD'
                },
                {
                    't':of_loc[:250],
                    'r':np.abs(of[:250]),
                    # 'type': 'scatter',
                    'mode': 'lines+markers',
                    'line': {'witdh': 10},
                    'name': 'OF'
                }],
        'layout':{
                    'radialaxis': { 'range': [0, 1000] },
                    'title': 'Optic Flow'
                 }
    }
    # print(of)
    json_msg = json.dumps(msg, cls=plotly.utils.PlotlyJSONEncoder)

    cherrypy.engine.publish('websocket-broadcast', json_msg)

    threading.Timer(0.100, publish_message, [vehicle]).start()


def getIpAdress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip

#   ### classes definition ###


class WebSocketHandler(WebSocket):

    def received_message(self, m):
        print 'message sent by someone : ' + m.data

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
