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

from server.msg_type import msg_tab, msg_tab_inv, msg_listener, password, MAV_CMD
from server.html_maker import get_html_code

# usefull function


def main():
    print 'starting up'

    global vehicle, IP_adr, number_of_client, client_handler, OBP_tab


    if not internet_on():
        print 'no internet connection'
        exit()

    IP_adr = getIpAdress()
    number_of_client = 0

    client_handler = ClientWebPlugin(cherrypy.engine).subscribe()

    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.config.update({'server.socket_host': IP_adr,
                            'server.socket_port': 8080})

    print 'waiting for drone'
    vehicle = dronekit.connect("udp:localhost:14550", rate=200, heartbeat_timeout=0)    # for local simulated drone
    # vehicle = dronekit.connect('/dev/ttyUSB0', baud=57600, rate=20)                       # for real drone
    print 'drone found, waiting ready'
    # vehicle.parameters['COM_RC_IN_MODE'] = 2;

    # listening on the arm message
    vehicle.add_attribute_listener('armed', arm_callback)

    # listening on all message (the call back is msg_handler)
    vehicle.add_message_listener('*', msg_handler)

    # getting OnBoard parameters
    OBP_tab = sorted(vehicle.parameters.keys())

    threading.Timer(5, send_plot_message).start() # start in 5 seconds

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


# check if number is an integer
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# return the string json message with specific code and data, code must be in the hashtable of msg_tab
def get_json_msg(code, data):

    if isinstance(data, list):
        msg = {
            'code' : msg_tab[code],
            'data' : data
        }
        return json.dumps(msg, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        print 'error: data format is not an list', data


# get the local IP adress, need to be connected to internet
def getIpAdress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip


# check internet connection
def internet_on():
        try:
            response=urllib2.urlopen('http://gmail.com',timeout=1)
            return True
        except urllib2.URLError as err:
            pass

        return False


# call back that handle all the message from the drone
def msg_handler(self, name, msg):
    new_time = time.time()

    if name not in msg_listener: #first time that we meet the message
        msg_listener[name] = [msg.to_dict(), 0, new_time]

    else:
        freq = 1/(new_time - msg_listener[name][2])
        if freq < 500:
            msg_listener[name] = [msg.to_dict(),round(freq, 2), new_time]


# send arm state to a client
def send_arm_state(client='everyone'):
    global vehicle
    send_data('ARM_STATE', [vehicle.armed], client)
    print 'sent arm state:' + str(vehicle.armed)


# send IP to the client
def send_IP(client='everyone'):
    global IP_adr
    send_data('IP', [IP_adr + ":8080"], client)
    print 'sent IP to ', client


# send all the GRAPH DATA to all the client every 5 seconds
def send_plot_message():
    send_data('GRAPH_DATA', [msg_listener])
    threading.Timer(5, send_plot_message).start() # every 5 seconds


# debug function: display the entire huge hash table msg_listener every 2 seconds (need to be call in the main function)
def test():
    testing_str = 'ATTITUDE'

    if testing_str in msg_listener:
        print get_json_msg('PLOT_DATA', [msg_listener]), '\n'

    threading.Timer(2, test).start()


# send data to a specified client, with a specified code and specified data
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


# call back that handle arm every time the drone send its arm state
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
        except KeyError: #if there is no client 'client_code'
            return -1


    def del_client(self, client_code):
        del self.clients[client_code]


class WebSocketHandler(WebSocket):

    def opened(self):
        global number_of_client
        self.client_code = number_of_client
        self.is_main_client = False
        cherrypy.engine.publish('add-client', self.client_code, self)

        self.plot = {
            'current_state' : False,
            'data' : [ ['ATTITUDE', 'pitch'],
                       ['ATTITUDE', 'roll'],
                       ['ATTITUDE', 'yaw'],
                       ['ATTITUDE', 'pitchspeed'] ],  # this field contain which value to send for the plot
            'rate' : 0.080
        }

        self.location = {
            'current_state' : False,
            'rate' : 1.000
        }


    # every time a message is received from a client, this function is called
    def received_message(self, m):
        # decrypt json format
        msg = json.loads(m.data)

        code = msg['code']
        data = msg['data']


        if code in msg_tab_inv:
            print 'receive command:', msg_tab_inv[code], 'from client number', self.client_code

        global vehicle

        if code == msg_tab['SWITCH_ARM']:
            if not self.is_main_client:
                send_arm_state()
                self.send_client_status()
                return

            vehicle.commands.upload()

            isarmed = vehicle.armed

            # change vehicle arm state
            isarmed = not isarmed
            vehicle.armed = isarmed
            vehicle.commands.upload()

            # waiting during 4 seconds for chagement of arm state
            t1 = time.time()
            while vehicle.armed != isarmed and time.time() - t1 < 4:
                pass

            if vehicle.armed != isarmed:
                print 'error : cannot change arm state, timout after 4 seconds'
                send_arm_state()

        elif code == msg_tab['GET_IP']:
            send_IP(self.client_code)

        elif code == msg_tab['GET_ARM']:
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

        elif code == msg_tab['PLOT_NEW_DATA']:
            if len(data) == 4 and len(data[0]) == 2 and len(data[1]) == 2 and len(data[2]) == 2 and len(data[3]) == 2:
                self.plot['data'] = data;

        elif code == msg_tab['GET_LOC']:
            if data[0] > 0:
                self.location['current_state'] = True
                self.location['rate'] = data[0]
                self.send_location()

            else:
                self.location['current_state'] = False
                self.send_location(True)

        elif code == msg_tab['GET_OBP']:
            if data[0] == 'ALL':
                send_data( 'OBP_VALUE_ALL', [ {value:vehicle.parameters[value]} for value in OBP_tab ], self.client_code)

            else:
                send_data('OBP_VALUE', [ data[0], vehicle.parameters[data[0]] ], self.client_code)

        elif code == msg_tab['SET_OBP']:

            id_str = str(data[0])
            try:
                value = float(data[1])
            except:
                print 'a wrong value was sent'

                if id_str in OBP_tab:
                    send_data('OBP_VALUE', [ id_str, vehicle.parameters[id_str] ], self.client_code)
                return

            if id_str in OBP_tab:

                if not self.is_main_client:
                    send_data('OBP_VALUE', [ id_str, vehicle.parameters[id_str] ], self.client_code)
                    self.send_client_status()
                    return

                vehicle.parameters[id_str] = value
                vehicle.commands.upload() # after this, "any writes are guaranteed to have completed"
                send_data('OBP_VALUE', [ id_str, vehicle.parameters[id_str] ], 'everyone')

                if vehicle.parameters[id_str] != value:
                    print 'failed to change parameter ', id_str

        elif code == msg_tab['SWITCH_STATE']:

            if self.is_main_client:
                self.is_main_client = False
                self.send_client_status(True)

            elif data[0] in password:
                self.is_main_client = True
                self.send_client_status(True)

            else:
                self.send_client_status(False)

        elif code == msg_tab['ASK_CLIENT_STATUS']:
            self.send_client_status()

        elif code == msg_tab['MAVLINK_COMMAND'] or code == msg_tab['MAVLINK_MESSAGE']:
            print 'here fine'
            if self.is_main_client:
                print 'here fine'
                if data[0] in MAV_CMD:
                    data[0] = MAV_CMD[data[0]]

                    print 'here fine:', data[0]

                elif not is_int(data[0]):
                    return

                # first parameter is the drone target, but dronekit automaticaly correct it
                vehicle.message_factory.command_long_send(0, 0, int(data[0]), int(data[1]), int(data[2]), int(data[3]),
                                                          float(data[4]), float(data[5]), float(data[6]), float(data[7]), float(data[8]))

                vehicle.commands.upload() # after this, "any writes are guaranteed to have completed"
                send_data('MAV_MSG_CONF', [])
            else:
                send_client_status()

        #elif code == msg_tab['MAVLINK_MESSAGE']:
        #    pass
            # for now, MAVLINK_MESSAGE and MAVLINK_COMMAND do the same thing

        elif code == msg_tab['GET_GRAPH_DATA']:
            send_data('GRAPH_DATA', [msg_listener], self.client_code)

        else:
            print 'receive unknown message :' + m.data


    def send_client_status(self, alert = False):
        if self.is_main_client:
            self.send(get_json_msg('SET_MAIN_CLIENT', [alert]));
        else:
            self.send(get_json_msg('SET_OBSERVER', [alert]));


    # manage the sending of the plot data every x seconds (usually x = 100ms)
    def send_plot_data(self):

        if self.plot['current_state'] and self.terminated == False:
            global vehicle

            json_msg = get_json_msg('PLOT_DATA',[msg_listener[self.plot['data'][0][0]][0][self.plot['data'][0][1]],
                                                 msg_listener[self.plot['data'][1][0]][0][self.plot['data'][1][1]],
                                                 msg_listener[self.plot['data'][2][0]][0][self.plot['data'][2][1]],
                                                 msg_listener[self.plot['data'][3][0]][0][self.plot['data'][3][1]]])
            self.send(json_msg)

            print 'sent one set of data'

            threading.Timer(self.plot['rate'], self.send_plot_data).start()

        else:
            print 'stop sending plot data'


    # manage the sending of the location every x seconds (usually x = 1s)
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

        #stop sending recursively data
        self.plot['current_state'] = False
        self.location['current_state'] = False


class Cherrypy_server(object):

    @cherrypy.expose
    def index(self):
        global IP_adr

        return get_html_code('ws://' + IP_adr + ':8080/ws')

    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))


if __name__ == '__main__':
    main()

###
# filename : server.py
#
# description: handle the server stuff in a ground control station. Handle the communication with one drone using
#   MAVLink message (dronekit library used) and the communication with many client (host a server using cherryPy)
#   send message using ws4py WebSocket protocol.
#
# Work made at the Labotory of Inteligent System at EPFL.
#
# Autor : Stephane Ballmer
#
# Last change: 15/06/2016
###
