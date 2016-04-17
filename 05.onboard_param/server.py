#    ### import ###

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


#    ### global var ###

global IP_adr
global vehicle
x = 0
trace = ['BIAS_ACC_X', 'BIAS_ACC_Y', 'BIAS_ACC_Z', 'BIAS_GYRO_X']


#    ### usefull function

def main():
    IP_adr = getIpAdress()

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.config.update({'server.socket_host': IP_adr,
                            'server.socket_port': 8080})

    # for local simulated drone
    vehicle = dronekit.connect("udp:localhost:14550")
    # vehicle = dronekit.connect('/dev/ttyUSB0', baud=57600)
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
    global x
    x += 0.1

    # msg = str(2*np.sin(x))+';'+str(2*(np.sin(x+np.pi/2)))+';'+str(2*(np.sin(x+np.pi)))+';'+str(2*(np.sin(x+np.pi*3/2)))

    # trace format example :
    # 156.096;765.9866;739.0985;34.97
    # trace1 ; trace2 ; trace3 ; trace4

    msg = ''

    for i in range(4):
        msg += str(vehicle.parameters[trace[i]]) + ';'

    cherrypy.engine.publish('websocket-broadcast', msg[:-1])

    threading.Timer(0.100, publish_message, [vehicle]).start()


def getIpAdress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip


#    ### classes definition ###


class WebSocketHandler(WebSocket):

    def received_message(self, m):
        print 'message sent by someone : ' + m.data

        if m.data[:16] == "CLIENT:ASK:TRACE" and len(m.data) > 19:
            trace[int(m.data[16]) - 1] = m.data[18:]

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

# possible to get those parameter by : sorted ( vehicle.parameters.keys() )

# possible message :
# CLIENT:ASK:TRACENB:BIAS_ACC_X
# CLIENT:ASK:TRACENB:BIAS_ACC_Y
# CLIENT:ASK:TRACENB:BIAS_ACC_Z
# CLIENT:ASK:TRACENB:BIAS_GYRO_X
# CLIENT:ASK:TRACENB:BIAS_GYRO_Y
# CLIENT:ASK:TRACENB:BIAS_GYRO_Z
# CLIENT:ASK:TRACENB:BIAS_MAG_X
# CLIENT:ASK:TRACENB:BIAS_MAG_Y
# CLIENT:ASK:TRACENB:BIAS_MAG_Z
# CLIENT:ASK:TRACENB:COM_RC_IN_MODE
# CLIENT:ASK:TRACENB:CTRL_CTRL_SRC
# CLIENT:ASK:TRACENB:ID_SYSID
# CLIENT:ASK:TRACENB:PITCH_R_D_CLIP
# CLIENT:ASK:TRACENB:PITCH_R_I_CLIP
# CLIENT:ASK:TRACENB:PITCH_R_KD
# CLIENT:ASK:TRACENB:PITCH_R_KI
# CLIENT:ASK:TRACENB:PITCH_R_KP
# CLIENT:ASK:TRACENB:POS_KP_ALT_BARO
# CLIENT:ASK:TRACENB:POS_KP_POS0
# CLIENT:ASK:TRACENB:POS_KP_POS1
# CLIENT:ASK:TRACENB:POS_KP_POS2
# CLIENT:ASK:TRACENB:POS_KP_VELB
# CLIENT:ASK:TRACENB:QF_KP_ACC
# CLIENT:ASK:TRACENB:QF_KP_MAG
# CLIENT:ASK:TRACENB:ROLL_R_D_CLIP
# CLIENT:ASK:TRACENB:ROLL_R_I_CLIP
# CLIENT:ASK:TRACENB:ROLL_R_KP
# CLIENT:ASK:TRACENB:ROLL_R_KI
# CLIENT:ASK:TRACENB:ROLL_R_KD
# CLIENT:ASK:TRACENB:SCALE_ACC_X
# CLIENT:ASK:TRACENB:SCALE_ACC_Y
# CLIENT:ASK:TRACENB:SCALE_ACC_Z
# CLIENT:ASK:TRACENB:SCALE_GYRO_X
# CLIENT:ASK:TRACENB:SCALE_GYRO_Y
# CLIENT:ASK:TRACENB:SCALE_GYRO_Z
# CLIENT:ASK:TRACENB:SCALE_MAG_X
# CLIENT:ASK:TRACENB:SCALE_MAG_Y
# CLIENT:ASK:TRACENB:SCALE_MAG_Z
# CLIENT:ASK:TRACENB:THRV_I_PREG
# CLIENT:ASK:TRACENB:THRV_KP
# CLIENT:ASK:TRACENB:THRV_KD
# CLIENT:ASK:TRACENB:THRV_SOFT
# CLIENT:ASK:TRACENB:VEL_CLIMBRATE
# CLIENT:ASK:TRACENB:VEL_CRUISESPEED
# CLIENT:ASK:TRACENB:VEL_DIST2VEL
# CLIENT:ASK:TRACENB:VEL_HOVERPGAIN
# CLIENT:ASK:TRACENB:VEL_HOVERDGAIN
# CLIENT:ASK:TRACENB:VEL_SOFTZONE
# CLIENT:ASK:TRACENB:VEL_WPT_PGAIN
# CLIENT:ASK:TRACENB:VEL_WPT_DGAIN
# CLIENT:ASK:TRACENB:YAW_R_D_CLIP
# CLIENT:ASK:TRACENB:YAW_R_I_CLIP
# CLIENT:ASK:TRACENB:YAW_R_KP
# CLIENT:ASK:TRACENB:YAW_R_KI
# CLIENT:ASK:TRACENB:YAW_R_KD
# CLIENT:ASK:TRACENB:YAW_R_P_CLMN
# CLIENT:ASK:TRACENB:YAW_R_P_CLMX

# example : CLIENT:ASK:TRACE1:THRV_KD"
