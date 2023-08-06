from connectivity.client.Client import Client

class MessageClient(Client):

    omrCallbackAttached = False
    
    def __init__(self):
        super().__init__()
    
    def sendMessage(self, message):
        ret = self.socket.sendall(bytes(self.flagBeginMsg + message + self.flagEndMsg, 'utf-8'))
        if ret == None:
            print('Message successfully sent')   
        else:
            print('Something went wrong sending the message')

    def setOnMessageReceivedCallback(self, callback):
        self.omrCallback = callback
        self.omrCallbackAttached = True

    def onMessageReceived(self, message):
        self.omrCallback(message)

    def isSetUp(self):
        return self.omrCallbackAttached