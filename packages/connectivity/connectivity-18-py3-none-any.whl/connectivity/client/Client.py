import os
import sys
import socket
import threading
from time import sleep
from abc import ABC
from multiprocessing import Process, Manager
from connectivity.MessageOrganizer import MessageOrganizer

class Client(MessageOrganizer, ABC):

    listening = True
    manager = Manager()

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
            t = threading.Thread(target=self.onConnected)
            # t.daemon = True
            t.start()
        else:
            print('Check callbacks!')

    def printP(self, txt):
        print(txt)
        sys.stdout.flush()

    def onConnected(self):
        listening = True
        while listening:
            ret = self.manager.Namespace()
            ret.value = 'default'
            p = Process(target=self.listenForData, args=(ret,))
            p.start()
            p.join()
            tag = ':'.join(ret.value.split(':')[:2])
            if tag + ':' == self.flagBeginMsg:
                msg = ''.join(ret.value.split(self.flagBeginMsg)[1:])
                self.onMessageReceived(msg)
            elif tag + ':' == self.flagBeginFile:
                fileName = ''.join(ret.value.split(self.flagBeginFile)[1:])
                self.onFileReceived(fileName)
            elif ret.value == self.flagError:
                self.disconnect()
                listening = False
        
    def listenForData(self, ret):
        while True:
            try:
                data = self.socket.recv(self.bufferSize)
                if not data:
                    # means: client disconnected, so let's close the unnecessary connection
                    self.printP('Disconnected from server')
                    # remove client from internal list of clients
                    ret.value = self.flagError
                    break
                else:
                    r = super().onDataReceived(data, ret=ret)
                    if r == True:
                        break
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.printP('Exception in Process:')
                self.printP(e)
                break

        print('Stopped listening for data')

    def onMessageReceived(self, msg):
        pass

    def onFileReceived(self, filePath):
        pass

    # Gets overridden
    def isSetUp(self):
        pass

    def disconnect(self):
        self.listening = False
        if self.socket:
            self.socket.close()
        else:
            print('Client is not connected')