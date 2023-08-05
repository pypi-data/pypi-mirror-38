import uuid
import time
import socket
import _thread as thread
from connectivity.MessageOrganizer import MessageOrganizer

class Server(MessageOrganizer):
    clients = []

    def __init__(self, address):
        super().__init__()
        self.address = address

    def startServer(self):
        if self.isSetUp():
            print('Setting up Server...')
            self.setupServer()
            thread.start_new_thread(self.listenForClients())
        else: print('The required callbacks have yet not been set. Please check...')

    def setupServer(self):
        self.socket = socket.socket()       # Create a socket object
        print('Host: ' + self.address[0])
        self.socket.bind(self.address)   # Bind to the port
        print('Server started!')

    def listenForClients(self):
        print ('Waiting for clients...')
        self.socket.listen(5)                   # Now wait for client connection.
        while True:
            conn, addr = self.socket.accept()   # Establish connection with client.
            thread.start_new_thread(self.onNewClient, (conn, addr))

    """
    When a new client connects, this method will be fired in a new thread.
    """
    def onNewClient(self, clientsocket, addr):
        # give each client a unique id
        uid = uuid.uuid4()
        # add client to the list of clients
        self.clients.append({
            'socket': clientsocket,
            'uid': uid,
            'name': 'Pymmel' # default name
        })
        print('Got connection from', addr)
        self.onConnect(uid, self)
        while True:
            data = clientsocket.recv(self.bufferSize)
            if not data:
                # means: client disconnected, so let's close the unnecessary connection
                print('Client with ID + \'' + str(uid) + '\' disconnected.')
                # remove client from internal list of clients
                self.removeClient(uid)
                clientsocket.close()
                break
            else:
                super().onDataReceived(data, uid=uid)

    def setClientName(self, uid, name):
        # TODO
        pass

    def getClients(self):
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

    def isSetUp(self):
        pass

    def removeClient(self, uid):
        for idx, cl in enumerate(self.clients):
            # print(cl[1])
            if cl['uid']==uid: 
                self.clients.pop(idx)
    
    def shutdownServer(self):
        print('Stopping server...')
        self.socket.close()