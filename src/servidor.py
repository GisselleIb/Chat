import socket
import sys
from _thread import *
class Servidor():

    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def setHost(self,host):
        self.host=host

    def setPort(self,port):
        self.port=port

    def getHost(self):
        return self.host

    def getPort(self):
        return self.port

    def conectaCliente(self):
        try:
            self.sock.bind((self.host,self.port))
            return True
        except socket.error:
            return False

    def servidorVivo(self):
        self.sock.listen(100)
        while 1:
            con,dir=self.sock.accept()
            print("Conectado a"+dir[0]+":"+str(dir[1]))
            start_new_thread(self.threadCliente,(con,))
            

    def threadCliente(self,con):
        while True:
            mensaje=con.recv(4096)
            respuesta= ':'+ mensaje.decode()
            if not mensaje:
                break
            con.sendall(mensaje)
            print(respuesta)
        con.close()

    def muerto(self):
        self.sock.close()
