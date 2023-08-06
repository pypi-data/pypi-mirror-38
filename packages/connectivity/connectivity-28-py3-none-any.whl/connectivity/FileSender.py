import os

from connectivity.MessageOrganizer import MessageOrganizer


class FileSender(MessageOrganizer):
    
    def sendFileViaSocket(self, filePath, socket):
        with open(filePath, 'rb') as fs: 
            try:
                size = os.path.getsize(filePath)
                _, fileName = os.path.split(filePath)
                socket.sendall(self.getFileBegin(fileName, size))
                socket.sendfile(fs)
                socket.sendall(self.getFileEnd())
                fs.close()
            except Exception as e:
                raise e
