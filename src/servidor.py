import socket
import sys
from usuario import Usuario
from sala import Sala
from _thread import *
class Servidor():
    salas=[]
    usuarios={} #diccionario de objetos usuario para saber su estado
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
        id=False
        while True:
            try:
                mensaje=con.recv(4096)
                if(mensaje):
                    msg=mensaje.decode()
                    print(msg)
                    id=self.manejaMensajes(msg,con,id)
                    print("Salida")
            except:
                continue
        con.close()

    def manejaMensajes(self,msg,con,id):
        print("entras")
        if("IDENTIFY" in msg):
            print("id")
            msg=msg.replace("IDENTIFY ","")
            id=self.identify(msg,con,id)
        elif not id:
            con.sendall("Necesitas identificarte primero".encode())
        else:
            if "PUBLICMESSAGE" in msg:
                print("public")
                msg=msg.replace("PUBLICMESSAGE ","")
                self.transmite(msg,con)
            elif "ROOMESSAGE" in msg:
                print("hola1")
                msg=msg.replace("ROOMESSAGE ","")
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
            elif "CREATEROOM" in msg:
                print("sala")
                msg=msg.replace("CREATEROOM ","")
                self.creaSala(msg,con)
            elif "INVITE" in msg:
                msg=msg.replace("INVITE ","")
                args=msg.split()
                lst=args[1:]
                self.invita(args[0],lst,con)
            elif "JOINROOM" in msg:
                print("join")
                msg=msg.replace("JOINROOM ","")
                self.unirse(msg,con)
            elif "DISCONNECT" in msg:
                msg=msg.replace("DISCONNECT","")
                for sala in self.salas:
                    sala.elimina(con)
            elif("STATUS" in msg):
                msg=msg.replace("STATUS","")
            elif("USERS" in msg):
                self.showUsuarios(con)
            else:
                con.sendall("Mensaje inválido".encode())

        return id

    def identify(self,msg,con,id):
        if not id:
            for usuario in self.usuarios:
                if usuario.nombre == msg:
                    con.sendall("Nombre en uso,escoge otro".encode())
                    return False
            us=Usuario(msg)
            self.usuarios[us]=con
            con.sendall("Identificación completada".encode())
            return True

    def showUsuarios(self,con):
        s=""
        for usuario in self.usuarios:
            s+=usuario.nombre + " "+ usuario.estado+ "\n"
        con.sendall(s.encode())

    def invita(self,nomsala,lista,conexion):
        print("invita")
        msg="Invitación a la sala: "+nomsala
        s=None
        for sala in self.salas:
            if sala.nombre == nomsala:
                s=sala
                if sala.dueño != conexion:
                    conexion.sendall("No eres dueño de la sala, no puedes invitar".encode())
                    return
        for us in lista:
            for usuario,cliente in self.usuarios.items():
                if(usuario.nombre == us):
                    cliente.sendall(msg.encode())
                    s.agregaInv(cliente)
                    break


    def unirse(self,s,con):
        print("uniendose")
        for sala in self.salas:
            if(sala.nombre == s):
                sala.agrega(con)

    def creaSala(self,nomsala,conexion):
        print("Creando sala")
        sala=Sala(nomsala,conexion)
        self.salas.append(sala)

    def transmiteChat(self,arr,conexion):
        msg=""
        for usuario,cliente in self.usuarios.items():
            if(cliente == conexion):
                msg=usuario.nombre+":"
                break
        i=1
        while i < len(arr):
            msg+=" "+arr[i]
            i+=1
        for sala in self.salas:
            if(sala.nombre == arr[0]):
                if not conexion in sala.clientes:
                    conexion.sendall("No puedes enviar mensajes a esta sala".encode())
                    return
                for cliente in sala.clientes:
                    if(cliente != conexion):
                        try:
                            cliente.sendall(msg.encode())
                        except e:
                            cliente.close()
                break


    def transmitePrivado(self,arr,con):
        mensaje=""
        us=None
        for usuario,cliente in self.usuarios.items():
            if(usuario.nombre == arr[0]):
                us=cliente
            if(cliente == con):
                mensaje=usuario.nombre+":"

        i=1
        while i < len(arr):
            mensaje+=" "+arr[i]
            i+=1
        try:
            us.sendall(mensaje.encode())
        except e:
            print("error")

    def transmite(self,respuesta,conexion):
        msg=''
        for usuario,cliente in self.usuarios.items():
            if(cliente == conexion):
                msg=usuario.nombre+": "
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
    serv=Servidor('192.168.1.70',port)
    serv.conectaCliente()
    serv.servidorVivo()
