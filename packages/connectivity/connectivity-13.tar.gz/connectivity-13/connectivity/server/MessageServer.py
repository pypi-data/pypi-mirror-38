import socket
import uuid
import _thread as thread
from connectivity.server.Server import Server

class MessageServer(Server):

    clients = []
    omrCallbackAttached = False

    def __init__(self, address):
        super().__init__(address)

    def setOnMessageReceivedListener(self, callback):
        self.onMessageReceivedCallback = callback
        self.omrCallbackAttached = True

    def onMessageReceived(self, uid, message):
        self.onMessageReceivedCallback(uid, message)

    def sendMessage(self, uid, message, name=None):
        for client in self.clients:
            if name and client['name'] == name:
                # Send message
                ret = client['socket'].sendall(bytes(self.flagBeginMsg + message + self.flagEndMsg, 'utf-8'))
                if ret == None:
                    print('message successfully sent')
                else:
                    print('Something went wrong sending the message')
                return
            elif client['uid'] == uid:
                # Send message
                ret = client['socket'].sendall(bytes(self.flagBeginMsg + message + self.flagEndMsg, 'utf-8'))
                if ret == None:
                    print('message successfully sent')
                else:
                    print('Something went wrong sending the message')
                return
        print('name or uid not found')


    def isSetUp(self):
        return self.omrCallbackAttached
