import socket
import sys
import select
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
        s=self.sock.recv(4096).decode()
        if(s == "Desconectando del Servidor"):
            print(s)
            return True
        else:
            return False
    def enviado(self):
        while True:
            lista=[sys.stdin, self.sock]
            r,w,e = select.select(lista,[],[])

            for socks in r:
                if(socks == self.sock):
                    mensaje = socks.recv(4096)
                    print(mensaje.decode())
                else:
                    mensaje = sys.stdin.readline()
                    self.sock.send(mensaje.encode())
                    sys.stdout.write("<TU>")
                    sys.stdout.write(mensaje)
        self.sock.close()
        sys.exit()
