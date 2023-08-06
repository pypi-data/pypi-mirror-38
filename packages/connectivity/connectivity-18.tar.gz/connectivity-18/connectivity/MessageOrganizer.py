import os
import time
from abc import ABC

class MessageOrganizer(ABC):

    # Constants:
    bufferSize = 1024
    flagBeginMsg = 'BEGIN:MSG:'
    flagEndMsg = ':END:MSG'
    flagBeginFile = 'BEGIN:FILE:'
    flagEndFile = ':END:FILE'
    flagError = 'ERROR'
    flagNameChange = 'NAMECHANGE:'
    flagInitClient = 'INITCLIENT:'
    flagInterrupt = 'INTERRUPT'
    cMsg = 'MSG'
    cFile = 'FILE'
    defaultDirectory = 'tmp/'
    defaultClientName = 'DefaultClientName'

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
            if bytes(self.flagBeginMsg, 'utf-8') in data:
                if bytes(self.flagEndMsg, 'utf-8') in data:
                    self.message = (data.decode('utf-8').split(self.flagBeginMsg)[1]).split(self.flagEndMsg)[0]
                    ret.value = self.flagBeginMsg + self.message
                    self.cleanupMessageTransfer()
                    return True
                self.lastType = self.cMsg
                self.lastChunk = data.decode('utf-8').split(self.flagBeginMsg)[1]
                return
            # Begin of File
            # Scheme:
            # BEGIN:FILE:<FileName>:<FileTotalSize>:<Data>:END:FILE
            elif bytes(self.flagBeginFile, 'utf-8') in data:
                self.lastType = self.cFile
                tags = data.decode('utf-8').split(':')
                self.lastFileName = tags[2]
                self.lastFileTotalSize = int(tags[3])
                self.lastFileStartTime = time.time()
                self.initFs(uid)
                splitTag = self.flagBeginFile + self.lastFileName + ':' + str(self.lastFileTotalSize) + ':'
                if bytes(self.flagEndFile, 'utf-8') in data:
                    firstChunk = data.decode('utf-8').split(splitTag)[1]
                    actualData = bytes(firstChunk.split(self.flagEndFile)[0], 'utf-8')
                    # print('Len: ' + str(len(actualData)))
                    self.lastFs.write(actualData)
                    progress = self.calculateProgress()
                    self.onFileProgress(uid, self.lastFileName, progress)
                    self.lastFs.close()
                    ret.value = self.flagBeginFile + self.lastFileName
                    self.cleanupFileTransfer()
                    return True
                else: # Gets triggered when no complete end flag is found
                    firstChunk = bytes(data.decode('utf-8').split(splitTag)[1], 'utf-8')
                    self.lastChunk = firstChunk
                    self.lastFileFirstChunk = firstChunk
                    return

        elif self.lastType == self.cMsg:
            # End of Message
            if bytes(self.flagEndMsg, 'utf-8') in bytes(self.lastChunk, 'utf-8') + data:
                self.message += (bytes(self.lastChunk, 'utf-8') + data).decode("utf-8").split(self.flagEndMsg)[0]
                ret.value = self.flagBeginMsg + self.message
                self.cleanupMessageTransfer()
                return True
            # Or still receiving data
            else:
                if self.lastChunk:
                    self.message += self.lastChunk
                self.lastChunk = data.decode('utf-8')

        elif self.lastType == self.cFile:
            lastData = self.lastChunk + data if self.lastChunk else data
            # End of File
            if bytes(self.flagEndFile, 'utf-8') in lastData:
                writeableData = bytes(lastData.decode('utf-8').split(self.flagEndFile)[0], 'utf-8')
                self.lastFs.write(writeableData)
                self.lastFileReceivedBytes += len(writeableData)
                #print('endFile')
                self.onFileProgress(uid, self.lastFileName, self.calculateProgress())
                self.lastFs.close()
                ret.value = self.flagBeginFile + self.lastFileName
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
            print('This should not happen... Check self.lastType!')

    def calculateProgress(self):
        timeDiff = (time.time() - self.lastFileStartTime)
        currentPercentage = self.lastFileReceivedBytes / self.lastFileTotalSize * 100
        progress = (currentPercentage, self.lastFileReceivedBytes, self.lastFileTotalSize, timeDiff)
        return progress

    def initFs(self, uid):
        path = self.defaultDirectory + str(uid) if uid else self.defaultDirectory
        # Check whether temporary directory exists
        if not os.path.exists(path):
            os.makedirs(path)
        # create FileStream and locally save it
        self.lastFs = open(path + '/' + self.lastFileName, 'wb') # TODO: Check if received File is binary


    def cleanupMessageTransfer(self):
        self.lastChunk = None
        self.lastType = None
        self.message = ''

    def getFileBegin(self, fileName, size):
        return bytes(self.flagBeginFile + fileName + ':' + str(size) + ':', 'utf-8')

    def getFileEnd(self):
        return bytes(self.flagEndFile, 'utf-8')

    def cleanupFileTransfer(self):
        self.lastChunk = None
        self.lastType = None
        self.lastFileName = None
        self.lastFileTotalSize = None
        self.lastFileFirstChunk = None
        self.lastFileReceivedBytes = 0
        self.lastFileStartTime = 0
        self.lastFs = None

    def onFileProgress(self, uid, fileName, progress): # progress: (percentage, received bytes, total bytes, time elapsed))
        pass
