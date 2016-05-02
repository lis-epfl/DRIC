
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

from server.msg_type import msg_tab, OBP_tab


#   ### global var ###


# global vehicle


# msg_tab = {
#     #server sending stuff
#     'PLOT_DATA'     : 0, # in data: 4 values for the plot
#     'ARM_STATE'     : 1, # 1 value, arm state
#     'IP'            : 2, # 1 string containing IP adress of server
#     'LOC'           : 3, # 3 value lat, lon, alt

#     #client sending stuff
#     'SWITCH_ARM'    : 100, # no value
#     'GET_ARM'       : 101, # no value
#     'GET_IP'        : 102, # no value
#     'PLOT_RATE'     : 103, # 1 int value : the rate in seconde, if rate=0, it means 'stop sending data'
#     'PLOT_NEW_DATA' : 104, # 4 values, no working for now
#     'GET_LOC'       : 105  # 1 value : if -1, just want to get the coord, is >0, want to get a this period the coord
# }




# usefull function


def main():
    
    global vehicle, IP_adr, number_of_client


    if not internet_on():
        print 'no internet connection'
        exit()

    IP_adr = getIpAdress()
    number_of_client = 0

    ClientWebPlugin(cherrypy.engine).subscribe()

    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.config.update({'server.socket_host': IP_adr,
                            'server.socket_port': 8080})
    
    vehicle = dronekit.connect("udp:localhost:14550", rate=20)    # for local simulated drone
    # vehicle = dronekit.connect('/dev/ttyUSB0', baud=57600, rate=20)
    print 'drone found, waiting ready'
    vehicle.wait_ready()
    # vehicle.parameters['COM_RC_IN_MODE'] = 2;

    vehicle.add_attribute_listener('armed', arm_callback)

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


def get_json_msg(code, data):

    if isinstance(data, list):
        msg = {
            'code' : msg_tab[code],
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


def send_arm_state(client='everyone'):
    global vehicle
    send_data('ARM_STATE', [vehicle.armed], client)
    print 'sent arm state:' + str(vehicle.armed)


def send_IP(client='everyone'):
    global IP_adr
    send_data('IP', [IP_adr + ":8080"], client)
    print 'sent IP to ', client


def send_data(code, data, client='everyone'):
    if not isinstance(code, str):
        print 'code need to be a string'
        return

    elif not isinstance(data, list):
        print 'data need to be an array'
        return


    if isinstance(client, str):
        if client in ['everyone', 'websocket-broadcast']:
            cherrypy.engine.publish('websocket-broadcast', get_json_msg(code, data))

    elif isinstance(client, list) and isinstance(client[0], int):
        for element in client:
            current = cherrypy.engine.publish('get-client', element).pop()
            current.send(get_json_msg(code, data))

    elif isinstance(client, int):
        current = cherrypy.engine.publish('get-client', client).pop()
        if current == -1:
            print 'error, client ', client, 'do not exist'
        else:
            current.send(get_json_msg(code, data))

    else:
        print 'send_Ip func: client type error'
        return


def arm_callback(self, attr, m):
    send_arm_state()


#   ### classes definition ###

class ClientWebPlugin(WebSocketPlugin):
    def __init__(self, bus):
        WebSocketPlugin.__init__(self, bus)
        self.clients = {}

    def start(self):
        WebSocketPlugin.start(self)
        self.bus.subscribe('add-client', self.add_client)
        self.bus.subscribe('get-client', self.get_client)
        self.bus.subscribe('del-client', self.del_client)
        # print 'start'

    def stop(self):
        WebSocketPlugin.stop(self)
        self.bus.unsubscribe('add-client', self.add_client)
        self.bus.unsubscribe('get-client', self.get_client)
        self.bus.unsubscribe('del-client', self.del_client)

    def add_client(self, client_code, websocket):
        self.clients[client_code] = websocket

    def get_client(self, client_code):
        try:
            return self.clients[client_code]
        except KeyError: #if there is no client 'clicent_code'
            return -1

    def del_client(self, client_code):
        del self.clients[client_code]


class WebSocketHandler(WebSocket):

    def opened(self):
        global number_of_client
        self.client_code = number_of_client
        cherrypy.engine.publish('add-client', self.client_code, self)

        self.plot = {
            'current_state' : False,
#           'data' : [ptch, roll, yaw, 0],      # this field contain which value to plot, no working for now
            'rate' : 0.080
        }

        self.location = {
            'current_state' : False,
            'rate' : 1.000
        }

        self.send_plot_data()

    def received_message(self, m):
        msg = json.loads(m.data)
        code = msg['code']
        data = msg['data']

        # print msg

        global vehicle

        if code == msg_tab['SWITCH_ARM']:
            print 'receive command: SWITCH_ARM from client ', self.client_code

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

        elif code == msg_tab['GET_IP']:
            print 'receive command: GET_IP from client ', self.client_code
            send_IP(self.client_code)

        elif code == msg_tab['GET_ARM']:
            print 'receive command: GET_ARM from client ', self.client_code
            send_arm_state()

        elif code == msg_tab['PLOT_RATE']:
            if data[0] <= 0:    # -1 means that the client don't want plot data anymore
                self.plot['current_state'] = False
                print 'receive order to stop sending plot data from client ', self.client_code

            elif self.plot['current_state'] == True:
                self.plot['rate'] = data[0]
                print 'receive order to change the rate of plot data from client ', self.client_code

            else:
                self.plot['rate'] = data[0]
                self.plot['current_state'] = True
                print 'receive order to send plot data from client ', self.client_code
                self.send_plot_data()

        elif code == msg_tab['GET_LOC']:
            if data[0] > 0:
                self.location['current_state'] = True
                self.location['rate'] = data[0]
                self.send_location()
                
            else:
                self.location['current_state'] = False
                self.send_location(True)

            print 'receive order to send location from client ', self.client_code

        elif code == msg_tab['GET_OBP']:
            if data[0] == 'ALL':
                send_data( 'OBP_VALUE_ALL', [ vehicle.parameters[value] for value in OBP_tab ], self.client_code)
            else:
                send_data('OBP_VALUE', [ data[0], vehicle.parameters[data[0]] ], self.client_code)

        elif code == msg_tab['SET_OBP']:

            id_str = str(data[0])
            value = float(data[1])

            if id_str in OBP_tab:
                # print 'receive parameter', id_str, 'to change to:', value, 'old value:', vehicle.parameters[id_str]
                # print '::::', str(data[0]), "::", float(data[1])
                # print type( str(data[0]) ), type( float(data[1]) )
                vehicle.parameters[id_str] = value
                # print 'uploading now'
                vehicle.commands.upload()
                send_data('OBP_VALUE', [ id_str, vehicle.parameters[id_str] ], self.client_code)

                if vehicle.parameters[id_str] != value:
                    print 'failed to change parameter ', id_str

        else:
            print 'receive unknown message :' + m.data 


    def send_plot_data(self):

        if self.plot['current_state'] and self.terminated == False:
            global vehicle

            json_msg = get_json_msg('PLOT_DATA', [vehicle.attitude.pitch, vehicle.attitude.roll, vehicle.attitude.yaw, 0])
            self.send(json_msg)

            threading.Timer(self.plot['rate'], self.send_plot_data).start()

        else:
            print 'stop sending plot data'


    def send_location(self, once=False):
        global vehicle

        if self.terminated:
            return

        if once or self.location['current_state']:
            send_data('LOC', [vehicle.location.global_frame.lat,
                              vehicle.location.global_frame.lon,
                              vehicle.location.global_frame.alt], self.client_code)

        if self.location['current_state']:
            threading.Timer(self.location['rate'], self.send_location).start()


    def closed(self, code, reason="A client left the room without a proper explanation."):
        print 'deconnexion of a client, reason :', reason
        cherrypy.engine.publish('del-client', self.client_code)
        self.plot['current_state'] = False


class Cherrypy_server(object):

    @cherrypy.expose
    def index(self):
        global IP_adr
        global number_of_client
        number_of_client += 1
        return file('public/index.html', 'r').read().format('ws://' + IP_adr + ':8080/ws', '%', '{', '}')

    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))


if __name__ == '__main__':
    main()