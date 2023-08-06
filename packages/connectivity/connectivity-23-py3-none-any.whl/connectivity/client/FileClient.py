import os

from connectivity.client.MessageClient import MessageClient
from connectivity.FileMover import FileMover
from connectivity.FileSender import FileSender
from connectivity import Constants as Const


class FileClient(MessageClient, FileMover, FileSender):

    ofrCallbackAttached = False
    orfpCallbackAttached = False

    def __init__(self):
        super().__init__()

    def sendFile(self, filePath):
        self.sendFileViaSocket(filePath, self.socket)

    def setOnFileReceivedCallback(self, callback):
        self.onFileReceivedCallback = callback
        self.ofrCallbackAttached = True

    def setOnReceivingFileProgressCallback(self, callback):
        self.onReceivingFileProgressCallback = callback
        self.orfpCallbackAttached = True

    def moveFileFromTmp(self, fileName, targetPath, override=False):
        sourcePath = Const.DEFAULT_DIR + fileName
        self.moveFile(sourcePath, targetPath, override=override)

    def onFileReceived(self, fileName):
        self.onFileReceivedCallback(fileName, self)

    def onFileProgress(self, uid, fileName, progress):
        self.onReceivingFileProgressCallback(fileName, progress)

    def isSetUp(self):
        return self.ofrCallbackAttached and self.orfpCallbackAttached and self.omrCallbackAttached
