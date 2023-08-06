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
        self.evaluateMessage(message)

    def evaluateMessage(self, message):
        if message.startswith(self.flagInitClient):
            content = message.split(self.flagInitClient)[1]
            self.uid = content.split(':')[0]
            self.name = ''.join(content.split(':')[1])
            print('Init: Name and UID have been set')
            print('Name:', self.name)
            print('UID:', self.uid)
        else:
            self.omrCallback(message)

    def changeName(self, name):
        self.sendMessage(self.flagNameChange + name)
        self.name = name
        print('Name successfully changed to:', name)

    def isSetUp(self):
        return self.omrCallbackAttached