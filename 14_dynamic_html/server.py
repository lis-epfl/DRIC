

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

from server.msg_type import msg_tab, msg_tab_inv, OBP_tab, msg_listener
from server.html_maker import get_html_code


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
    
    global vehicle, IP_adr, number_of_client, client_handler


    if not internet_on():
        print 'no internet connection'
        exit()

    IP_adr = getIpAdress()
    number_of_client = 0

    client_handler = ClientWebPlugin(cherrypy.engine).subscribe()

    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.config.update({'server.socket_host': IP_adr,
                            'server.socket_port': 8080})
    
    vehicle = dronekit.connect("udp:localhost:14550", rate=20)    # for local simulated drone
    # vehicle = dronekit.connect('/dev/ttyUSB0', baud=57600, rate=20)
    print 'drone found, waiting ready'
    vehicle.wait_ready()
    # vehicle.parameters['COM_RC_IN_MODE'] = 2;

    vehicle.add_attribute_listener('armed', arm_callback)
    vehicle.add_message_listener('*', msg_handler)
    test()

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


def msg_handler(self, name, msg):
    new_time = time.time()

    if name not in msg_listener:
        print 'new entry:', name
        msg_listener[name] = [msg.to_dict(), 0, new_time]

    else:
        freq = 1/(new_time - msg_listener[name][2])
        msg_listener[name] = [msg.to_dict(), round(freq, 2), new_time]

    

def send_arm_state(client='everyone'):
    global vehicle
    send_data('ARM_STATE', [vehicle.armed], client)
    print 'sent arm state:' + str(vehicle.armed)


def send_IP(client='everyone'):
    global IP_adr
    send_data('IP', [IP_adr + ":8080"], client)
    print 'sent IP to ', client

# def send_


def test():
    testing_str = 'ATTITUDE'

    if testing_str in msg_listener:
        print get_json_msg('PLOT_DATA', [msg_listener]), '\n'
        # print 'frequency:', msg_listener[testing_str][1], '\n'

    threading.Timer(2, test).start()



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
        self.main_client_code = -1

    def start(self):
        WebSocketPlugin.start(self)
        self.bus.subscribe('add-client', self.add_client)
        self.bus.subscribe('get-client', self.get_client)
        self.bus.subscribe('del-client', self.del_client)
        self.bus.subscribe('get_main-client', self.get_main_client_num)
        self.bus.subscribe('switch-state', self.switch_state)

    def stop(self):
        WebSocketPlugin.stop(self)
        self.bus.unsubscribe('add-client', self.add_client)
        self.bus.unsubscribe('get-client', self.get_client)
        self.bus.unsubscribe('del-client', self.del_client)
        self.bus.unsubscribe('get_main-client', self.get_main_client_num)
        self.bus.unsubscribe('switch-state', self.switch_state)

    def add_client(self, client_code, websocket):
        self.clients[client_code] = websocket

        if self.main_client_code == -1:
            self.main_client_code = client_code
            self.clients[client_code].is_main_client = True
            # send_data('SET_MAIN_CLIENT', [], self.main_client)
        else:
            pass
            # send_data('SET_OBSERVER', [], client_code)

    def get_client(self, client_code):
        try:
            return self.clients[client_code]
        except KeyError: #if there is no client 'client_code'
            return -1

    def del_client(self, client_code):
        del self.clients[client_code]

        if len(self.clients) == 0: # no client connected
            self.main_client_code = -1
        
        elif self.main_client_code == client_code: # some client remain and a new main has to be set
            self.main_client_code = self.clients.itervalues().next().client_code
            self.clients[self.main_client_code].is_main_client = True
            send_data('SET_MAIN_CLIENT', [True], self.main_client_code)

        print "number of client remaining: ", len(self.clients), " main_client_code: ", self.main_client_code

    def get_main_client_num(self):
        return self.main_client_code

    def switch_state(self, client_code):
        if len(self.clients) <= 1:  # if 1 client or less, there is only one main and no observer obviously...
            return -1

        elif client_code == self.main_client_code: # if the guy want to stop being the main client 
            for code_temp in self.clients: # search for an available client to switch statuts with
                if code_temp == self.main_client_code:
                    continue
                else:
                    break

            self.main_client_code = code_temp
            self.clients[client_code].is_main_client = False
            self.clients[self.main_client_code].is_main_client = True
            return self.main_client_code #return the new main client

        else: # if the guy want to be the main and the main client confirmed ! 
            temp = self.main_client_code
            self.clients[self.main_client_code].is_main_client = False
            self.clients[client_code].is_main_client = True
            self.main_client_code = client_code
            return temp #return the old main client

        return -1 # if for any raison we come here, it must be a failure


class WebSocketHandler(WebSocket):

    def opened(self):
        global number_of_client
        self.client_code = number_of_client
        self.is_main_client = False
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

    def received_message(self, m):
        msg = json.loads(m.data)

        code = msg['code']
        data = msg['data']

        # print 'check status:', code in msg_tab

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

            # waiting during 5 seconds for chagement of arm state
            t1 = time.time()
            while vehicle.armed != isarmed and time.time() - t1 < 5:
                pass

            if vehicle.armed != isarmed:
                print 'error : cannot change arm state, timout after 5 seconds'
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
                send_data( 'OBP_VALUE_ALL', [ vehicle.parameters[value] for value in OBP_tab ], self.client_code)
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
                vehicle.commands.upload()
                send_data('OBP_VALUE', [ id_str, vehicle.parameters[id_str] ], 'everyone')

                if vehicle.parameters[id_str] != value:
                    print 'failed to change parameter ', id_str


        elif code == msg_tab['SWITCH_STATE']:
            # print 'receive SWITCH order from', self.client_code, ' status: ', self.is_main_client

            if self.is_main_client:
                #if the guy is the main and want to become observer, no need to ask confirmation
                new_main_client = cherrypy.engine.publish('switch-state', self.client_code).pop()

                if new_main_client == -1: # it failed
                    self.send_client_status(new_main_client, False)
                else: #it success
                    self.send_client_status(new_main_client, True) #send both new status, if no status changed, one is send

            else:
                old_main = cherrypy.engine.publish('get_main-client').pop()
                send_data('ASK_CHANGE', [self.client_code], old_main)


        elif code == msg_tab['ANSW_CHANGE_STATUS']: #data[0] is the client code, data[1] is the answer: true or false
            if len(data) != 2:
                print 'error in package type ANSW_CHANGE_STATUS'
                return

            elif data[1] == False: # main said No to change
                print 'Controler refuse to switch'
                send_data('SET_OBSERVER', [False], data[0]) #sending status OBSERVER to the guy that wanted to change

            elif data[1] == True: # main accept !
                print 'Switching observer and controler'

                success = cherrypy.engine.publish('switch-state', data[0]).pop()

                #now the old main and new observer is self.client_code and success
                #now the old observer and new main is data[0]

                if success == -1:   #it failed
                    self.send_client_status(data[0], False)
                else:
                    self.send_client_status(data[0], True)


        elif code == msg_tab['ASK_CLIENT_STATUS']:
            self.send_client_status()

        else:
            print 'receive unknown message :' + m.data 


    def send_client_status(self, other_client_id = -1, alert = False):
        if self.is_main_client:
            self.send(get_json_msg('SET_MAIN_CLIENT', [alert]));
        else:
            self.send(get_json_msg('SET_OBSERVER', [alert]));

        if other_client_id >= 0:
            main_id = cherrypy.engine.publish('get_main-client').pop()

            if other_client_id == main_id:
                send_data('SET_MAIN_CLIENT', [alert], other_client_id)
            else:
                send_data('SET_OBSERVER', [alert], other_client_id)


    def send_plot_data(self):

        if self.plot['current_state'] and self.terminated == False:
            global vehicle

            json_msg = get_json_msg('PLOT_DATA', [vehicle.attitude.pitch, vehicle.attitude.roll, vehicle.attitude.yaw, 0])
            self.send(json_msg)

            print 'sent one set of data'

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
        # return file('public/index.html', 'r').read().format('ws://' + IP_adr + ':8080/ws', '%', '{', '}')
        return get_html_code('ws://' + IP_adr + ':8080/ws')

    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))


if __name__ == '__main__':
    main()
