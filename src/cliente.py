import socket
import sys
import select
from usuario import Usuario
class Cliente():
    """"Clase cliente que conectara con el servidor
    y se enviara los mensajes del usuario al servidor
    que le dara una respuesta
    """

    def __init__(self,host,port):
        """Constructor de la clase, crea un socket TCP
        Parámetros
        host"""
        self.host=host
        self.port=port
        self.user=Usuario("")
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
            print("Bienvenido,para poder enviar mensajes "+
            "identificate con tu nombre de usuario con el comando -id nombre")
            return True
        except socket.timeout:
            return False

    def desconectado(self):
        d="DISCONNECT"
        self.sock.send(d.encode())
        self.sock.close()

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
                    self.comandos(mensaje)
        self.sock.close()
        sys.exit()

    def ayuda(self):
        print(" -r usuario mensaje: Envía un mensaje privado al usuario especificado"+
        "\n -d : Cierra la sesión" +
        "\n -s sala: Ingresa a la sala de chat especificada" +
         "o la crea si no existe" +
         "\n -u : Enseña todos los usuarios conectados y sus estados"+
         "\n -p mensaje : Envía un mensaje a todos los usuarios conectados")

    def comandos(self,mensaje):
        men=mensaje.split()
        if(men[0] == "-id"):
            self.identifica(men[1])
        elif(men[0] == "-r"):
            self.enviaPrivado(mensaje)
        elif(men[0] == "-help"):
            self.ayuda()
        elif(men[0] == "-d"):
            self.desconectado()
        elif(men[0] == "-y"):
            self.unirse(men[1])
        elif (men[0] == "-i" ):
            self.invita(men[1:])
        elif(men[0] == "-s"):
            try:
                self.salaChat(men[1])
            except IndexError:
                print("Escribe un nombre para la sala")
        elif(men[0] == "-u"):
            self.showUsuarios()
        elif(men[0] == "-st"):
            self.status()
        elif(men[0] == "-rm"):
            if(len(men) < 3):
                print("Mensaje Inválido")
            else:
                self.enviaSala(men[1:])
        else:
            self.enviaTodos(mensaje)

    def status(self):
        msg="STATUS"
        self.sock.send(msg.encode())

    def identifica(self,nombre):
        id="IDENTIFY "+nombre
        self.user.nombre=nombre
        self.sock.send(id.encode())

    def invita(self,l):
        msg="INVITE"
        for usuario in l:
            msg+=" "+usuario
        self.sock.send(msg.encode())

    def showUsuarios(self):
        msg="USERS"
        self.sock.send(msg.encode())

    def enviaTodos(self,mensaje):
        msg="PUBLICMESSAGE "+ mensaje
        self.sock.send(msg.encode())
        sys.stdout.write("<TU>")
        sys.stdout.write(mensaje)

    def salaChat(self,sala):
        msg="CREATEROOM "+sala
        self.sock.send(msg.encode())

    def unirse(self,sala):
        msg="JOINROOM "+sala
        self.sock.send(msg.encode())

    def enviaSala(self,arr):
        msg="ROOMMESSAGE"
        if(len(arr) < 2):
            print("Inválido")
        for s in arr:
            msg+=" "+s
        self.sock.send(msg.encode())

    def enviaPrivado(self,mensaje):
        msg="MESSAGE "+ mensaje
        msg=msg.replace("-r","")
        self.sock.send(msg.encode())
