import os
import shutil
from pathlib import Path

from connectivity.FileMover import FileMover
from connectivity.FileSender import FileSender
from connectivity.server.MessageServer import MessageServer
from connectivity import Constants as Const


class FileServer(MessageServer, FileMover, FileSender):
    
    ofrCallbackAttached = False
    orfpCallbackAttached = False

    def __init__(self, ip=Const.DEFAULT_SERVER_IP, port=Const.DEFAULT_PORT):
        super().__init__(ip=ip, port=port)

    def sendFile(self, uid, filePath):
        self.sendFileViaSocket(filePath, self.getSocketByUid(uid))
    
    def setOnFileReceivedCallback(self, callback):
        self.ofrCallbackAttached = True
        self.onFileReceivedCallback = callback

    def setOnReceivingFileProgressCallback(self, callback):
        self.orfpCallbackAttached = True
        self.onReceivingFileProgressCallback = callback

    def onFileReceived(self, uid, fileName):
        self.onFileReceivedCallback(uid, fileName, self)

    def onFileProgress(self, uid, fileName, progress):
        self.onReceivingFileProgressCallback(uid, fileName, progress)

    def moveFileFromTmp(self, uid, fileName, targetPath, override=False):
        sourceDir = Const.DEFAULT_DIR + uid + '/'
        self.moveFile(sourceDir + fileName, targetPath, override=override)
        Path(sourceDir).rmdir()

    def isSetUp(self):
        return self.ofrCallbackAttached and self.orfpCallbackAttached and self.omrCallbackAttached
