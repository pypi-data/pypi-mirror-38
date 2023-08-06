import os
import socket
import sys
import threading
from abc import ABC
from multiprocessing import Manager, Process
from time import sleep

from connectivity.MessageOrganizer import MessageOrganizer
from connectivity.Exceptions import MissingCallbackException, ClientNotConnectedException
from connectivity import Constants as Const


class Client(MessageOrganizer, ABC):

    listening = True
    manager = Manager()

    def __init__(self):
        super().__init__()
        self.socket = None

    def connect(self, ip=Const.DEFAULT_CLIENT_IP, port=Const.DEFAULT_PORT):
        # check if all required callbacks are set
        # if True, connect to the server
        if self.isSetUp():
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((ip, port))
            except Exception as e:
                print(e)
                return
            # start new thread which takes care about managing received messages/files
            t = threading.Thread(target=self.onConnected)
            t.start()
        else:
            raise MissingCallbackException('Some required callbacks are missing. Please check!')

    def onConnected(self):
        listening = True
        while listening:
            ret = self.manager.Namespace()
            ret.value = 'default'
            p = Process(target=self.listenForData, args=(ret,))
            p.start()
            p.join()
            tag = ':'.join(ret.value.split(':')[:2])
            if tag + ':' == Const.BEGIN_MSG:
                msg = ''.join(ret.value.split(Const.BEGIN_MSG)[1:])
                self.onMessageReceived(msg)
            elif tag + ':' == Const.BEGIN_FILE:
                fileName = ''.join(ret.value.split(Const.BEGIN_FILE)[1:])
                self.onFileReceived(fileName)
            elif ret.value == Const.ERROR:
                self.disconnect()
                listening = False
        
    def listenForData(self, ret):
        while True:
            try:
                data = self.socket.recv(Const.BUFFER_SIZE)
                if not data:
                    # means: client disconnected, so return an error
                    ret.value = Const.ERROR
                    break
                else:
                    r = super().onDataReceived(data, ret=ret)
                    if r == True:
                        break
            except KeyboardInterrupt:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
                break
            except Exception as e:
                break

    # OVERRIDE
    def onMessageReceived(self, msg):
        pass

    # OVERRIDE
    def onFileReceived(self, filePath):
        pass

    # OVERRIDE
    def isSetUp(self):
        pass

    def disconnect(self):
        self.listening = False
        if self.socket:
            self.socket.close()
        else:
            raise ClientNotConnectedException('Client is not connected. First connect, then disconnect!')