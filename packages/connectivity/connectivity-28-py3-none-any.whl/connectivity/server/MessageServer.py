import socket
import uuid

import _thread as thread
from connectivity.server.Server import Server
from connectivity.Exceptions import ClientNotFoundException, MessageSendingException
from connectivity import Constants as Const


class MessageServer(Server):

    omrCallbackAttached = False

    def __init__(self, ip=Const.DEFAULT_SERVER_IP, port=Const.DEFAULT_PORT):
        super().__init__(ip=ip, port=port)

    def setOnMessageReceivedListener(self, callback):
        self.onMessageReceivedCallback = callback
        self.omrCallbackAttached = True

    def onMessageReceived(self, uid, msg):
        self.evaluateMessage(uid, msg)

    def evaluateMessage(self, uid, msg):
        if msg.startswith(Const.NAME_CHANGE):
            name = ''.join(msg.split(Const.NAME_CHANGE)[1])
            self.changeName(uid, name)
        else:
            self.onMessageReceivedCallback(uid, msg)

    def changeName(self, uid, name):
        for client in self.clients:
            if client['uid'] == uid:
                client['name'] = name
                return
        raise ClientNotFoundException('UID not found for name change')

    def sendMessage(self, message, uid=None, name=None):
        if uid or name:
            for client in self.clients:
                if name and client['name'] == name or uid and client['uid'] == uid:
                    # Send message
                    ret = client['socket'].sendall(bytes(Const.BEGIN_MSG + message + Const.END_MSG, 'utf-8'))
                    if ret != None:
                        raise MessageSendingException('Something went wrong sending the message. Error: ' + ret)
                    return
            raise ClientNotFoundException('name/uid not found')
        else:
            for client in self.clients:
                ret = client['socket'].sendall(bytes(Const.BEGIN_MSG + message + Const.END_MSG, 'utf-8'))
                if ret != None:
                    raise MessageSendingException('Something went wrong sending the message. Error: ' + ret)

    def initClient(self, uid):
        # Send an init message to the client like this:
        # "INITCLIENT:<UID>:<DefaultName>"
        self.sendMessage(Const.INIT_CLIENT + uid + ':' + Const.DEFAULT_CLIENT_NAME, uid=uid)

    def isSetUp(self):
        return self.omrCallbackAttached
