import socket
import sys
from _thread import *
class Servidor():
    clientes=[]
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
        while True:
            print("Servidor Vivo")
            con,dir=self.sock.accept()
            self.clientes.append(con)
            print("Conectado a"+dir[0]+":"+str(dir[1]))
            start_new_thread(self.threadCliente,(con,dir))


    def threadCliente(self,con,dir):
        while True:
            try:
                mensaje=con.recv(4096)
                if(mensaje.decode() == "Salir"):
                    self.con.send("Desconectando del Servidor")
                    break
                if(mensaje):
                    respuesta= str(dir[0])+":"+str(dir[1])+ ":"+mensaje.decode()
                    print(respuesta)
                    #considerar meter aqui la clase usuario y tomar su nombre...
                    self.transmite(respuesta.encode(),con)
            except:
                continue
        con.close()

    def transmite(self,respuesta,conexion):
            for cliente in self.clientes:
                if(cliente != conexion):
                    try:
                        cliente.sendall(respuesta)
                    except e:
                        cliente.close()

    def muerto(self):
        self.sock.close()


if __name__ == "__main__":
    port=int(input("Introduce el puerto:\n"))
    serv=Servidor(socket.gethostname(),port)
    serv.conectaCliente()
    serv.servidorVivo()
