import socket
import _thread as thread
from time import sleep
from connectivity.MessageOrganizer import MessageOrganizer

class Client(MessageOrganizer):
    def __init__(self):
        super().__init__()
        self.socket = None
    def connect(self, address):
        if self.isSetUp():
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect(address)
            except Exception as e:
                print(e)
                return
            print('Connected to Server!')
            # Start Listening for data
            thread.start_new_thread(self.listenForData, ())
        else:
            print('Check callbacks!')

    def listenForData(self):
        print('Listening for Data')
        while True:
            data = self.socket.recv(self.bufferSize)
            if not data:
                # means: client disconnected, so let's close the unnecessary connection
                print('Disconnected from server')
                # remove client from internal list of clients
                self.socket.close()
                self.socket = None
                break
            else:
                super().onDataReceived(data)

    # Gets overridden
    def isSetUp(self):
        pass

    def disconnect(self):
        if self.socket:
            self.socket.close()
        else:
            print('Client is not connected')