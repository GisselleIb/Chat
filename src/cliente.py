import socket
import sys
class Cliente():

    def __init__(self,host,port):
        self.host=host
        self.port=port
        try:
            self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.error as e:
            print("Error al crear socket")
            sys.exit()

        def setHost(self,host):
            self.host=host

        def setPort(self,port):
            self.port=port

        def getHost(self):
            return self.host

        def getPort(self):
            return self.port

    def seConecto(self):
        try:
            self.sock.connect((self.host,self.port))
            print("cliente conectado")
            return True
        except socket.timeout:
            return False
    def desconectado(self):
        pass

    def enviado(self):
        print("Bienvenido, escribe tu mensaje!:"+"\n")
        while True:
            mensaje=input()
            try:
                self.sock.sendall(mensaje.encode())
                print(mensaje)
                return True
            except socket.error:
                print("Falla al enviar el mensaje")
                sys.exit()
                return False
    def respuesta(self):
        respuesta=self.sock.recv(4096)
        print(respuesta)
