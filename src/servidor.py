import socket
import sys
from _thread import *
class Servidor():
    salas={"global":[]}
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
            self.salas["global"].append(con)
            print("Conectado a"+dir[0]+":"+str(dir[1]))
            start_new_thread(self.threadCliente,(con,dir))


    def threadCliente(self,con,dir):
        while True:
            try:
                mensaje=con.recv(4096)
                if(mensaje):
                    msg=mensaje.decode()
                    if(msg == "Salir"):
                        self.con.send("Desconectando del Servidor")
                        break
                    elif("Sala: " in msg):
                        self.salaChat(msg,con)
                    elif("-p" in msg):
                        transmitePrivado(msg,con)
                    else:
                        respuesta= str(dir[0])+":"+str(dir[1])+ ":"+msg
                        print(respuesta)
                    #considerar meter aqui la clase usuario y tomar su nombre...
                        self.transmite(mensaje,con)
            except:
                continue
        con.close()

    def salaChat(self,sala,conexion):
        if not sala in self.salas:
            self.salas[sala]=[conexion]
        else:
            self.salas[sala].append(conexion)

    def transmitePrivado(self,mensaje,con):
        try:
            mens=con.recv(4096)
            self.clientes[mensaje].sendall(mens)
        except e:
            print("Error")

    def transmite(self,respuesta,conexion):
        for sala,clientes in self.salas.items():
            for cliente in clientes:
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
