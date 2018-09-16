import socket
import sys
from usuario import Usuario
from sala import Sala
from _thread import *
class Servidor():
    salas=[]
    usuarios={}
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
            print("Conectado a"+dir[0]+":"+str(dir[1]))
            start_new_thread(self.threadCliente,(con,dir))


    def threadCliente(self,con,dir):
        while True:
            try:
                mensaje=con.recv(4096)
                if(mensaje):
                    msg=mensaje.decode()
                    print(msg)
                    self.manejaMensajes(msg,con,dir)
                    print("Salida")
            except:
                continue
        con.close()

    def manejaMensajes(self,msg,con,dir):
        print("entras")
        if("IDENTIFY" in msg):
            msg=msg.replace("IDENTIFY ","")
            self.usuarios[msg]=con
            con.sendall("Identificación completada".encode())
        elif "PUBLICMESSAGE" in msg:
            print("public")
            msg=msg.replace("PUBLICMESSAGE ","")
            self.transmite(msg,con)
        elif "ROOMMESSAGE" in msg:
            print("hola1")
            msg=msg.replace("ROOMMESSAGE ","")
            arr=msg.split()
            self.transmiteChat(arr,con)
        elif "MESSAGE" in msg :
            print("hola")
            if(len(msg) < 3):
                con.sendall("Mensaje Inválido".encode())
            else:
                msg=msg.replace("MESSAGE ","")
                arr=msg.split()
                self.transmitePrivado(arr,con)
        elif "CREATROOM" in msg:
            if(len(msg) > 2):
                con.sendall("Mensaje Inválido")
            else:
                msg=msg.replace("CREATROOM ","")
                self.creaSala(msg,con)
        elif "INVITE" in msg:
            msg=msg.replace("INVITE ","")
            args=msg.split()
            lst=args[1:]
            self.invita(args[0],lst)
        elif "JOINROOM" in msg:
            msg=msg.replace("JOINROOM ","")
            self.unirse(self,msg,con)
        elif "DISCONNECT" in msg:
            msg=msg.replace("DISCONNECT","")
            for sala in self.salas:
                sala.elimina(con)
        elif("STATUS" in msg):
            msg=msg.replace("STATUS","")
        elif("USERS" in msg):
            self.showUsuarios(con)

    def showUsuarios(self,con):
        s=""
        for usuario in self.usuarios:
            s+=usuario + "\n"
        con.sendall(s)
        return s

    def invita(self,nomsala,lista):
        msg="Invitación a la sala: "+nomsala
        for usuario in lista:
            if(usuario in self.usuarios):
                self.usuarios[usuario].sendall(msg.encode())

    def unirse(self,s,con):
        for sala in self.salas:
            if(sala.nombre == s):
                sala.agrega(con)
                msg="Te has unido a: "+s
                con.send(msg.encode())

    def creaSala(self,nomsala,conexion):
        sala=Sala(nomsala,conexion)
        sala.agrega(conexion)
        self.salas.append(sala)


    def transmiteChat(self,mensaje,conexion):
        arr=mensaje.split()
        i=1
        msg=""
        while i < len(arr):
            msg+=arr[i]
        for sala in self.salas:
            if(sala.nombre == arr[0]):
                for cliente in sala.clientes:
                    if(cliente != conexion):
                        try:
                            cliente.sendall(msg.encode())
                        except e:
                            cliente.close()
                break


    def transmitePrivado(self,arr,con):
        print("privado")
        if(arr[0] in self.usuarios):
            mensaje=""
            for usuario,cliente in self.usuarios.items():
                if(cliente == con):
                    mensaje=usuario+":"
                    break
            us=self.usuarios[arr[0]]
            i=1
            while i < len(arr):
                mensaje+=" "+arr[i]
                print(mensaje)
                i+=1
            try:
                us.sendall(mensaje.encode())
            except e:
                us.close()

    def transmite(self,respuesta,conexion):
        msg=''
        for usuario in self.usuarios:
            if(self.usuarios[usuario] == conexion):
                msg=usuario+": "
                break
        msg+= respuesta
        for usuario,cliente in self.usuarios.items():
            if(cliente != conexion):
                try:
                    cliente.sendall(msg.encode())
                except e:
                    cliente.close()

    def muerto(self):
        self.sock.close()


if __name__ == "__main__":
    port=int(input("Introduce el puerto:\n"))
    serv=Servidor('',port)
    serv.conectaCliente()
    serv.servidorVivo()
