import socket
import sys
from usuario import Usuario
from sala import Sala
from _thread import *
class Servidor():
    salas=[]
    usuarios={}
    """Clase Servidor encargada de procesar los mensajes
    enviados por el cliente.
    """
    def __init__(self,host,port):
        """Constructor de la clase, crea un socket TCP
        Parámetros
        ----------
        host : str
           La dirección IP del servidor.
        port : int
           El puerto del servidor.
        sock : socket
           Socket con el que se hará la conexión
        """
        self.host=host
        self.port=port
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def conectaCliente(self):
        """Hace el bind con la ip y puerto.
        """
        try:
            self.sock.bind((self.host,self.port))
            self.servidorVivo()
            return True
        except socket.error:
            return False

    def servidorVivo(self):
        """Pone al servidor en marcha y comienza a esperar
        por conexiones, para luego meterlas en un hilo
        """
        self.sock.listen(100)
        while True:
            print("Servidor Vivo")
            con,dir=self.sock.accept()
            print("Conectado a"+dir[0]+":"+str(dir[1]))
            start_new_thread(self.threadCliente,(con,dir))


    def threadCliente(self,con,dir):
        """El hilo que maneja el cliente,recibe mensajes
        del cliente
        Parámetros
        ----------
        con : socket
           Conexión con el cliente.
        dir : (str,int)
           Dirección del cliente.
        """
        id=False
        while True:
            try:
                mensaje=con.recv(1096)
                if(mensaje):
                    msg=mensaje.decode()
                    print(msg)
                    id=self.manejaMensajes(msg,con,id)
                    print("Salida")
            except:
                continue
        con.close()

    def manejaMensajes(self,msg,con,id):
        """Procesa los mensajes recibidos del cliente
        Parámetros
        ----------
        msg : str
           Mensaje a procesar.
        con : socket
           Conexión con el cliente.
        id : Bool
           Bandera para comprobar si el usuario se identifico
        """
        if("IDENTIFY" in msg):
            msg=msg.replace("IDENTIFY ","")
            id=self.identify(msg,con,id)
        elif not id:
            con.sendall("Necesitas identificarte primero".encode())
        else:
            if "PUBLICMESSAGE" in msg:
                msg=msg.replace("PUBLICMESSAGE ","")
                self.transmite(msg,con)
            elif "ROOMESSAGE" in msg:
                msg=msg.replace("ROOMESSAGE ","")
                arr=msg.split()
                self.transmiteChat(arr,con)
            elif "MESSAGE" in msg :
                if(len(msg) < 3):
                    con.sendall("Mensaje Inválido".encode())
                else:
                    msg=msg.replace("MESSAGE ","")
                    arr=msg.split()
                    self.transmitePrivado(arr,con)
            elif "CREATEROOM" in msg:
                msg=msg.replace("CREATEROOM ","")
                self.creaSala(msg,con)
            elif "INVITE" in msg:
                msg=msg.replace("INVITE ","")
                args=msg.split()
                lst=args[1:]
                self.invita(args[0],lst,con)
            elif "JOINROOM" in msg:
                msg=msg.replace("JOINROOM ","")
                self.unirse(msg,con)
            elif "DISCONNECT" in msg:
                for usuario,cliente in self.usuarios:
                    if(cliente == con):
                        del self.usuarios[usuario]
                        con.close()
                for sala in self.salas:
                    sala.elimina(con)
            elif("STATUS" in msg):
                msg=msg.replace("STATUS ","")
                print(msg)
                if(msg == "ACTIVE" or msg == "BUSY" or msg == "AWAY"):
                    for usuario in self.usuarios:
                        if self.usuarios[usuario] == con :
                            usuario.asignaEstado(msg)
            elif("USERS" in msg):
                self.showUsuarios(con)
            else:
                con.sendall("Mensaje inválido".encode())

        return id

    def identify(self,msg,con,id):
        """Identifica al usuario y lo guarda en el diccionario
        Parámetros
        ----------
        msg : str
            nombre del usuario.
        con : socket
            Conexión con el cliente.
        id : Bool
           Bandera para marcar que el usuario se identificó.
        """
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
        """Enseña los usuarios conectados y su status.
        Parámetros
        ----------
        con : socket
            Conexión con el cliente.
        """
        s=""
        for usuario in self.usuarios:
            s+=usuario.nombre + " "+ usuario.estado+ "\n"
        con.sendall(s.encode())

    def invita(self,nomsala,lista,conexion):
        """Invita a la sala a la lista de usuario.
        Parámetros
        ----------
        nomsala : str
           Nombre de la sala
        lista : [str]
            Lista de usuarios a invitar
        conexión : socket
                Conexión con el cliente.
        """
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
        """Une al usuario a la sala indicada.
        Parámetros
        ----------
        s : str
            Nombre de la sala
         con : socket
            Conexión con el cliente.
        """
        for sala in self.salas:
            if(sala.nombre == s):
                sala.agrega(con)

    def creaSala(self,nomsala,conexion):
        """Crea una sala nueva
        Parámetros
        ----------
        nomsala : str
            Nombre de la sala
        conexion : socket
           Conexión con el cliente.
        """
        sala=Sala(nomsala,conexion)
        self.salas.append(sala)

    def transmiteChat(self,arr,conexion):
        """Transmite un mensaje a la sala de chat indicada
        Parámetros
        ----------
        arr : [str]
        conexion : socket
           Conexión con el cliente
        """
        msg=arr[0]
        for usuario,cliente in self.usuarios.items():
            if(cliente == conexion):
                msg+=usuario.nombre+":"
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
        """Transmite un mensaje privado a un usuario
        Parámetros
        ----------
        arr :[str]
            Lista que contiene el usuario al que va dirigido
            y el mensaje
        con : socket
           Conexión con el cliente
        """
        mensaje="privado"
        us=None
        for usuario,cliente in self.usuarios.items():
            if(usuario.nombre == arr[0]):
                us=cliente
            if(cliente == con):
                mensaje+=usuario.nombre+":"

        i=1
        while i < len(arr):
            mensaje+=" "+arr[i]
            i+=1
        try:
            us.sendall(mensaje.encode())
        except e:
            print("error")

    def transmite(self,respuesta,conexion):
        """Transmite un mensaje global
        Parámetros
        ----------
        respuesta : str
            Mensaje que se va a transmitir
        conexion : socket
           Conexión con el cliente.
        """
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
    serv=Servidor('0.0.0.0',port)
    serv.conectaCliente()
    serv.servidorVivo()
