import os
import socket
import sys
import threading
import uuid
from abc import ABC
from multiprocessing import Manager, Process

from connectivity.MessageOrganizer import MessageOrganizer
from connectivity.Exceptions import MissingCallbackException, ServerNotRunningException
from connectivity import Constants as Const


class Server(MessageOrganizer, ABC):
    
    clients = []
    manager = Manager()

    def __init__(self, ip=Const.DEFAULT_SERVER_IP, port=Const.DEFAULT_PORT):
        super().__init__()
        self.ip = ip
        self.port = port
        self.socket = None
        self.running = False

    def startServer(self):
        if self.isSetUp():
            self.setupServer()
            self.running = True
            t = threading.Thread(target=self.listenForClients)
            t.start()
        else: 
            raise MissingCallbackException('The required callbacks have yet not been set. Please check...')

    def setupServer(self):
        self.socket = socket.socket()               # Create a socket object
        self.socket.bind((self.ip, self.port))      # Bind to the port

    def listenForClients(self):
        self.socket.listen(5)                       # Now wait for client connection.
        while self.running:
            try:
                conn, addr = self.socket.accept()   # Establish connection with client.
                t = threading.Thread(target=self.onNewClient, args=(conn, addr))
                t.start()
            except:
                pass

    """
    When a new client connects, this method will be fired in a new thread.
    """
    def onNewClient(self, clientsocket, addr):
        # give each client a unique id
        uid = str(uuid.uuid4())
        # add client to the list of clients
        self.clients.append({
            'socket': clientsocket,
            'uid': uid,
            'name': Const.DEFAULT_CLIENT_NAME # default name
        })
        self.onConnect(uid, self)
        self.initClient(uid)
        listening = True
        while listening:
            ret = self.manager.Namespace()
            ret.value = 'default'
            p = Process(target=self.listenForData, args=(uid, clientsocket, ret))
            p.start()
            p.join()
            tag = ':'.join(ret.value.split(':')[:2])
            if tag + ':' == Const.BEGIN_MSG:
                msg = ''.join(ret.value.split(Const.BEGIN_MSG)[1:])
                self.onMessageReceived(uid, msg)
            elif tag + ':' == Const.BEGIN_FILE:
                fileName = ''.join(ret.value.split(Const.BEGIN_FILE)[1:])
                self.onFileReceived(uid, fileName)
            elif ret.value == Const.ERROR:
                clientsocket.close()
                self.removeClient(uid)
                listening = False
        

    def listenForData(self, uid, clientsocket, ret):
        while True:
            try:
                data = clientsocket.recv(Const.BUFFER_SIZE)
                if not data:
                    # means: client disconnected, so let's close the unnecessary connection
                    ret.value = Const.ERROR
                    break
                else:
                    r = super().onDataReceived(data, uid=uid, ret=ret)
                    if r == True:
                        break
            except KeyboardInterrupt:
                clientsocket.shutdown(socket.SHUT_RDWR)
                clientsocket.close()
                break
            except Exception as e:
                break

    # OVERRIDE
    def onMessageReceived(self, uid, msg):
        pass

    # OVERRIDE
    def onFileReceived(self, uid, fileName):
        pass

    # OVERRIDE
    def initClient(self, uid):
        pass

    # OVERRIDE
    def isSetUp(self):
        pass

    def setClientName(self, uid, name):
        # TODO
        pass

    def getClients(self):
        # TODO
        pass

    def getClientUid(self, name):
        # TODO
        pass

    def getSocketByUid(self, uid):
        client = self.getClientByUid(uid)
        return client['socket'] if client else None

    def getClientByUid(self, uid):
        for client in self.clients:
            if client['uid'] == uid:
                return client
        return None
    
    def setOnConnect(self, connectListener):
        self.onConnect = connectListener

    def removeClient(self, uid):
        for idx, cl in enumerate(self.clients):
            if cl['uid'] == uid: 
                self.clients.pop(idx)
    
    def shutdownServer(self):
        if not self.running:
            raise ServerNotRunningException('Server is not running anymore')
            return
        self.running = False
        for client in self.clients:
            try:
                client['socket'].close()
            except OSError as e:
                pass
        try: 
            self.socket.close()
        except OSError:
            pass
