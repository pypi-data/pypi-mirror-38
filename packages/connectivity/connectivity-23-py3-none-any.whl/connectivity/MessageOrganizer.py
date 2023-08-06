import os
import time
from abc import ABC

from connectivity import Constants as Const
from connectivity.Exceptions import MOException


class MessageOrganizer(ABC):

    def __init__(self):
        # Variables:
        self.message = ''
        self.lastChunk = None
        self.lastType = None
        self.lastFs = None
        self.lastFileName = None
        self.lastFileFirstChunk = None
        self.lastFileStartTime = 0
        self.lastFileTotalSize = 0
        self.lastFileReceivedBytes = 0

    def onDataReceived(self, data, uid=None, ret=None):
        if self.lastType == None:
            # Begin of Message
            # Scheme:
            # BEGIN:MSG:<Message>:END:MSG
            if bytes(Const.BEGIN_MSG, 'utf-8') in data:
                if bytes(Const.END_MSG, 'utf-8') in data:
                    self.message = (data.decode('utf-8').split(Const.BEGIN_MSG)[1]).split(Const.END_MSG)[0]
                    ret.value = Const.BEGIN_MSG + self.message
                    self.cleanupMessageTransfer()
                    return True
                self.lastType = Const.TYPE_MSG
                self.lastChunk = data.decode('utf-8').split(Const.BEGIN_MSG)[1]
                return
            # Begin of File
            # Scheme:
            # BEGIN:FILE:<FileName>:<FileTotalSize>:<Data>:END:FILE
            elif bytes(Const.BEGIN_FILE, 'utf-8') in data:
                self.lastType = Const.TYPE_FILE
                tags = data.decode('utf-8').split(':')
                self.lastFileName = tags[2]
                self.lastFileTotalSize = int(tags[3])
                self.lastFileStartTime = time.time()
                self.initFs(uid)
                splitTag = Const.BEGIN_FILE + self.lastFileName + ':' + str(self.lastFileTotalSize) + ':'
                if bytes(Const.END_FILE, 'utf-8') in data:
                    firstChunk = data.decode('utf-8').split(splitTag)[1]
                    actualData = bytes(firstChunk.split(Const.END_FILE)[0], 'utf-8')
                    self.lastFs.write(actualData)
                    progress = self.calculateProgress()
                    self.onFileProgress(uid, self.lastFileName, progress)
                    self.lastFs.close()
                    ret.value = Const.BEGIN_FILE + self.lastFileName
                    self.cleanupFileTransfer()
                    return True
                else: # Gets triggered when no complete end flag is found
                    firstChunk = bytes(data.decode('utf-8').split(splitTag)[1], 'utf-8')
                    self.lastChunk = firstChunk
                    self.lastFileFirstChunk = firstChunk
                    return

        elif self.lastType == Const.TYPE_MSG:
            # End of Message
            if bytes(Const.END_MSG, 'utf-8') in bytes(self.lastChunk, 'utf-8') + data:
                self.message += (bytes(self.lastChunk, 'utf-8') + data).decode("utf-8").split(Const.END_MSG)[0]
                ret.value = Const.BEGIN_MSG + self.message
                self.cleanupMessageTransfer()
                return True
            # Or still receiving data
            else:
                if self.lastChunk:
                    self.message += self.lastChunk
                self.lastChunk = data.decode('utf-8')

        elif self.lastType == Const.TYPE_FILE:
            lastData = self.lastChunk + data if self.lastChunk else data
            # End of File
            if bytes(Const.END_FILE, 'utf-8') in lastData:
                writeableData = bytes(lastData.decode('utf-8').split(Const.END_FILE)[0], 'utf-8')
                self.lastFs.write(writeableData)
                self.lastFileReceivedBytes += len(writeableData)
                self.onFileProgress(uid, self.lastFileName, self.calculateProgress())
                self.lastFs.close()
                ret.value = Const.BEGIN_FILE + self.lastFileName
                self.cleanupFileTransfer()
                return True
            # Or still receiving data
            else:
                if self.lastChunk:
                    self.lastFs.write(self.lastChunk)
                    self.lastFileReceivedBytes += len(self.lastChunk)
                    self.onFileProgress(uid, self.lastFileName, self.calculateProgress())
                self.lastChunk = data
        else:
            raise MOException('This should not happen... Check self.lastType!')

    def calculateProgress(self):
        timeDiff = (time.time() - self.lastFileStartTime)
        currentPercentage = self.lastFileReceivedBytes / self.lastFileTotalSize * 100
        progress = (currentPercentage, self.lastFileReceivedBytes, self.lastFileTotalSize, timeDiff)
        return progress

    def initFs(self, uid):
        path = Const.DEFAULT_DIR + uid if uid else Const.DEFAULT_DIR
        # Check whether temporary directory exists
        if not os.path.exists(path):
            os.makedirs(path)
        # create FileStream and locally save it
        self.lastFs = open(path + '/' + self.lastFileName, 'wb')


    def cleanupMessageTransfer(self):
        self.lastChunk = None
        self.lastType = None
        self.message = ''

    def getFileBegin(self, fileName, size):
        return bytes(Const.BEGIN_FILE + fileName + ':' + str(size) + ':', 'utf-8')

    def getFileEnd(self):
        return bytes(Const.END_FILE, 'utf-8')

    def cleanupFileTransfer(self):
        self.lastChunk = None
        self.lastType = None
        self.lastFileName = None
        self.lastFileTotalSize = None
        self.lastFileFirstChunk = None
        self.lastFileReceivedBytes = 0
        self.lastFileStartTime = 0
        self.lastFs = None

    # progress: (percentage, received bytes, total bytes, time elapsed))
    def onFileProgress(self, uid, fileName, progress):
        pass
