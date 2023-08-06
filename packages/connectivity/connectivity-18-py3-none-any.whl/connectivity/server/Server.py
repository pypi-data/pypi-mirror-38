import os
import sys
import uuid
import time
import socket
import threading
from abc import ABC
from ctypes import c_char_p
from multiprocessing import Process, Queue, Manager, active_children
from connectivity.MessageOrganizer import MessageOrganizer

class Server(MessageOrganizer, ABC):
    
    clients = []
    manager = Manager()
    serverDC = 'SRV_DC'
    clientDC = 'CL_DC'

    def __init__(self, address):
        super().__init__()
        self.address = address

    def startServer(self):
        if self.isSetUp():
            print('Setting up Server...')
            self.setupServer()
            self.running = True
            t = threading.Thread(target=self.listenForClients)
            # t.daemon = True
            t.start()
        else: print('The required callbacks have yet not been set. Please check...')

    def setupServer(self):
        self.socket = socket.socket()       # Create a socket object
        print('Host: ' + self.address[0])
        self.socket.bind(self.address)      # Bind to the port
        print('Server started!')

    def listenForClients(self):
        print ('Waiting for clients...')
        self.socket.listen(5)               # Now wait for client connection.
        while self.running:
            try:
                conn, addr = self.socket.accept()   # Establish connection with client.
                t = threading.Thread(target=self.onNewClient, args=(conn, addr))
                # t.daemon = True
                t.start()
            except:
                pass
                

    # def listenForGlobalChanges(self):
    #     while self.queue.get() != self.serverDC:
    #         pass
    #     self.running = False

    def printP(self, txt):
        print(txt)
        sys.stdout.flush()

    """
    When a new client connects, this method will be fired in a new process.
    """
    def onNewClient(self, clientsocket, addr):
        # give each client a unique id
        uid = uuid.uuid4()
        # add client to the list of clients
        self.clients.append({
            'socket': clientsocket,
            'uid': uid,
            'name': self.defaultClientName # default name
        })
        print('Got connection from', addr)
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
            if tag + ':' == self.flagBeginMsg:
                msg = ''.join(ret.value.split(self.flagBeginMsg)[1:])
                self.onMessageReceived(uid, msg)
            elif tag + ':' == self.flagBeginFile:
                fileName = ''.join(ret.value.split(self.flagBeginFile)[1:])
                self.onFileReceived(uid, fileName)
            elif ret.value == self.flagError:
                clientsocket.close()
                self.removeClient(uid)
                listening = False
        

    def listenForData(self, uid, clientsocket, ret):
        self.printP('Listening for data in new process')
        while True:
            try:
                data = clientsocket.recv(self.bufferSize)
                if not data:
                    # means: client disconnected, so let's close the unnecessary connection
                    self.printP('Client with ID + \'' + str(uid) + '\' disconnected.')
                    ret.value = self.flagError
                    break
                else:
                    r = super().onDataReceived(data, uid=uid, ret=ret)
                    if r == True:
                        break
            except KeyboardInterrupt:
                # ret.value = self.flagError
                clientsocket.shutdown(socket.SHUT_RDWR)
                clientsocket.close()
                break
            except Exception as e:
                self.printP('Exception in Process:')
                self.printP(e)
                break
        # self.printP('Stopping to listen for data from \'' + str(uid) + '\'')


    def onMessageReceived(self, uid, msg):
        pass

    def onFileReceived(self, uid, fileName):
        pass

    def initClient(self, uid):
        pass

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
            # print(cl[1])
            if cl['uid']==uid: 
                self.clients.pop(idx)
    
    def shutdownServer(self):
        print('Stopping server...')
        if not self.running:
            print('Server is already stopped')
            return
        self.running = False
        for client in self.clients:
            try:
                client['socket'].close()
            except:
                print('Could not close client socket')
        self.socket.close()
        print('Server stopped')