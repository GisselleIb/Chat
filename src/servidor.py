import socket
import sys
class Servidor():

    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.sock=socket.socket()

    def setHost(self,host):
        self.host=host

    def setPort(self,port):
        self.port=port

    def getHost(self):
        return self.host

    def getPort(self):
        return self.port

    def conectaCliente(self):
        return False

    def muerto(self):
        return True

    def escucha(self):
        return ''


    def acepta(self):
        pass

    def enviaRespuesta(self):
        pass

    def lee(self):
        pass
