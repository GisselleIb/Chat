import socket
import sys
import select
class Cliente():
    """"Clase cliente que conectara con el servidor
    y se enviara los mensajes del usuario al servidor
    que le dara una respuesta
    """

    def __init__(self,host,port,user):
        """Constructor de la clase, crea un socket TCP
        Parámetros
        host"""
        self.host=host
        self.port=port
        self.user=user
        try:
            self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.user.setDir(self.sock.getsockname())
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
            print("Bienvenido, escribe -ayuda para ver "+
            "todos los comandos disponibles")
            return True
        except socket.timeout:
            return False

    def desconectado(self):
        d="DISCONNECT"
        self.sock.send(d.encode())
        self.sock.close()

    def enviado(self):
        id="IDENTIFY"+self.user.nombre
        self.sock.send(id.encode())
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
         "\n -p mensaje : Envía un mensaje a todos los usuarios conectados")

    def comandos(self,mensaje):
        men=mensaje.split()
        if(men[0] == "-r"):
            self.enviaPrivado(men)
        elif(men[0] == "-help"):
            self.ayuda()
        elif(men[0] == "-d"):
            self.desconectado()
        elif(men[0] == "-y"):
            self.unirse(men[1])
        elif(men[0] == "-s"):
            try:
                self.salaChat(men[1])
            except IndexError:
                print("Escribe un nombre para la sala")
        else:
            self.enviaTodos(mensaje)

    def enviaTodos(self,mensaje):
        msg="PUBLICMESSAGE"+self.user.nombre +":"+ mensaje
        self.sock.send(msg.encode())
        sys.stdout.write("<TU>")
        sys.stdout.write(mensaje)

    def salaChat(self,sala):
        msg="CREATROOM"+sala
        self.sock.send(msg.encode())

    def unirse(self,sala):
        msg="JOINROOM"+sala
        self.sock.send(msg.encode())

    def enviaSala(self,arr):
        msg="ROOMMESSAGE"
        for s in arr:
            msg+=""+s
        self.sock.send(msg.encode())

    def enviaPrivado(self,mensaje):
        msg="MESSAGE"+self.user.nombre+":"
        for s in mensaje:
            msg+=" "+s
        msg=msg.replace("-r","")
        self.sock.send(msg.encode())
