import socket
import uuid
import _thread as thread
from connectivity.server.Server import Server

class MessageServer(Server):

    # clients = []
    omrCallbackAttached = False

    def __init__(self, address):
        super().__init__(address)

    def setOnMessageReceivedListener(self, callback):
        self.onMessageReceivedCallback = callback
        self.omrCallbackAttached = True

    def onMessageReceived(self, uid, msg):
        self.evaluateMessage(uid, msg)

    def evaluateMessage(self, uid, msg):
        if msg.startswith(self.flagNameChange):
            name = ''.join(msg.split(self.flagNameChange)[1])
            self.changeName(uid, name)
        else:
            self.onMessageReceivedCallback(uid, message)

    def changeName(self, uid, name):
        for client in self.clients:
            if client['uid'] == uid:
                prevName = client['name']
                client['name'] = name
                print('Name of Client \'' + prevName + '\' changed to \'' + name + '\'')
                return
        print('UID not found for name change')

    def sendMessage(self, message, uid=None, name=None):
        for client in self.clients:
            if name and client['name'] == name:
                # Send message
                ret = client['socket'].sendall(bytes(self.flagBeginMsg + message + self.flagEndMsg, 'utf-8'))
                if ret == None:
                    print('message successfully sent')
                else:
                    print('Something went wrong sending the message')
                return
            elif uid and client['uid'] == uid:
                # Send message
                ret = client['socket'].sendall(bytes(self.flagBeginMsg + message + self.flagEndMsg, 'utf-8'))
                if ret == None:
                    print('message successfully sent')
                else:
                    print('Something went wrong sending the message')
                return
        print('name/uid not found or not given')

    def initClient(self, uid):
        # Send an init message to the client like this:
        # "INITCLIENT:<UID>:<DefaultName>"
        self.sendMessage(self.flagInitClient + str(uid) + ':' + self.defaultClientName, uid=uid)

    def isSetUp(self):
        return self.omrCallbackAttached
