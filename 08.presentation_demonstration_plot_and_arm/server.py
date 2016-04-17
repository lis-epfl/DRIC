
#   ### import ###

# system lib
import os
import os.path
import socket

# internet lib
import urllib2

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

# global vehicle
msg_tab = {
    #server sending stuff

    'PLOT_DATA' : 0,    # 4 values for the plot
    'ARM_STATE' : 1,    # 1 value, arm state
    'IP'        : 2,    # 1 string containing IP adress of server

    #client sending stuff
    'SWITCH_ARM' : 100, # no value
    'GET_ARM'    : 101, # no value
    'GET_IP'     : 102  # no value
}


# usefull function


def main():
    global vehicle, IP_adr

    if not internet_on():
        print 'no internet connection'
        exit()

    IP_adr = getIpAdress()

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.config.update({'server.socket_host': IP_adr,
                            'server.socket_port': 8080})
    
    vehicle = dronekit.connect("udp:localhost:14550", rate=20)    # for local simulated drone
    # vehicle = dronekit.connect('/dev/ttyUSB0', baud=57600, rate=20)
    print 'drone found, waiting ready'
    vehicle.wait_ready()
    # vehicle.parameters['COM_RC_IN_MODE'] = 2;

    vehicle.add_attribute_listener('armed', arm_callback)
    publish_message()

    # init_message()

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
    global vehicle

    json_msg = get_json_msg(msg_tab['PLOT_DATA'], [vehicle.attitude.pitch, vehicle.attitude.roll, vehicle.attitude.yaw, 0])

    cherrypy.engine.publish('websocket-broadcast', json_msg)

    threading.Timer(0.080, publish_message).start()


def get_json_msg(code, data):

    if isinstance(data, list):
        msg = {
            'code' : code,
            'data' : data
        }
        return json.dumps(msg, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        print 'error: data format is not an list', data


def getIpAdress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip


def internet_on():
        try:
            response=urllib2.urlopen('http://gmail.com',timeout=1)
            return True
        except urllib2.URLError as err:
            pass

        return False


def send_arm_state():
    global vehicle
    print 'sent arm state:' + str(vehicle.armed)

    cherrypy.engine.publish('websocket-broadcast', get_json_msg(msg_tab['ARM_STATE'], [vehicle.armed]))


def send_IP():
    global IP_adr
    # cherrypy.engine.publish('websocket-broadcast', TextMessage("IP:" + IP_adr + ":8080"))
    cherrypy.engine.publish('websocket-broadcast', get_json_msg(msg_tab['IP'], [IP_adr + ":8080"]) )


def arm_callback(self, attr, m):
    send_arm_state()


#   ### classes definition ###


class WebSocketHandler(WebSocket):

    def received_message(self, m):
        msg = json.loads(m.data)
        # print 'receive : ' + m.data
        global vehicle

        if msg['code'] == msg_tab['SWITCH_ARM']:
            print 'receive command: SWITCH_ARM'

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
                send_arm_state()

        elif msg['code'] == msg_tab['GET_IP']:
            print 'receive command: GET_IP'
            send_IP()

        elif msg['code'] == msg_tab['GET_ARM']:
            print 'receive command: GET_ARM'
            send_arm_state()

        else:
            print 'receive unknown message :' + m.data


    def closed(self, code, reason="A client left the room without a proper explanation."):
        print 'deconnexion of a client, reason :', reason


class Cherrypy_server(object):

    @cherrypy.expose
    def index(self):
        global IP_adr
        return file('public/html/index.html', 'r').read() % {'WS_ADR_GET': 'ws://' + IP_adr + ':8080/ws'}

    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))


if __name__ == '__main__':
    main()
