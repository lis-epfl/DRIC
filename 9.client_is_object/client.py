# cherrypy lib
import cherrypy

# websocket communication lib
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage


class Client(object):
    def __init__(self, client):
        # self.client_ = client
        pass

    def send(self, message):
        # client.send(message)
        pass

