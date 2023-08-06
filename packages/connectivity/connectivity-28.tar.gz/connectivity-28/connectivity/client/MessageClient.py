from connectivity.client.Client import Client
from connectivity.Exceptions import MessageSendingException
from connectivity import Constants as Const


class MessageClient(Client):

    omrCallbackAttached = False
    
    def __init__(self):
        super().__init__()
    
    def sendMessage(self, message):
        ret = self.socket.sendall(bytes(Const.BEGIN_MSG + message + Const.END_MSG, 'utf-8'))
        if ret != None: 
            raise MessageSendingException('Something went wrong sending the message. Error: ' + ret)

    def setOnMessageReceivedCallback(self, callback):
        self.omrCallback = callback
        self.omrCallbackAttached = True

    def onMessageReceived(self, message):
        self.evaluateMessage(message)

    def evaluateMessage(self, message):
        if message.startswith(Const.INIT_CLIENT):
            content = message.split(Const.INIT_CLIENT)[1]
            self.uid = content.split(':')[0]
            self.name = ''.join(content.split(':')[1])
        else:
            self.omrCallback(message)

    def changeName(self, name):
        self.sendMessage(Const.NAME_CHANGE + name)
        self.name = name

    def isSetUp(self):
        return self.omrCallbackAttached
