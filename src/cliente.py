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
        host
        port
        user
        vista
        """
        self.host=host
        self.port=port
        self.user=Usuario("")
        self.escuchas=[]
        try:
            self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except OSError as e:
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
            self.actualiza("Bienvenido,para poder enviar mensajes "+
            "identificate con tu nombre de usuario con el comando -id nombre")
            return True
        except socket.timeout:
            return False

    def desconectado(self):
        d="DISCONNECT"
        self.sock.send(d.encode())
        sys.exit()
        self.sock.close()

    def enviado(self):
        while True:
            lista=[sys.stdin, self.sock]
            r,w,e = select.select(lista,[],[])

            for socks in r:
                if(socks == self.sock):
                    mensaje = socks.recv(1096)
                    self.actualiza(mensaje.decode())

        self.sock.close()
        sys.exit()

    def ayuda(self):
        s=" -r usuario mensaje: Envía un mensaje privado al usuario especificado"+ \
        "\n -d : Cierra la sesión" +\
        "\n -s sala: Crea una nueva sala de chat con el nombre especificado" +\
         "\n -y sala: Te unes a la sala de chat especificada, pero tienes"+\
         "\n que haber sido invitado primero"+\
         "\n -u : Enseña todos los usuarios conectados y sus estados"+\
         "\n -p mensaje : Envía un mensaje a todos los usuarios conectados"
        self.vista.recibido(s)

    def comandos(self,mensaje):
        if not mensaje:
            return
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
            try:
                self.unirse(men[1])
            except IndexError:
                self.actualiza("Escribe un nombre para la sala")
        elif (men[0] == "-i" ):
            try:
                self.invita(men[1:])
            except IndexError:
                self.actualiza("Escribe un nombre para la sala")
        elif(men[0] == "-s"):
            try:
                self.salaChat(men[1])
            except IndexError:
                self.actualiza("Escribe un nombre para la sala")
        elif(men[0] == "-u"):
            self.showUsuarios()
        elif(men[0] == "-st"):
            self.status()
        elif(men[0] == "-rm"):
            if(len(men) < 3):
                self.actualiza("Mensaje Inválido")
            else:
                self.enviaSala(men[1:])
        else:
            self.enviaTodos(mensaje)

    def actualiza(self,evento):
        for escucha in self.escuchas:
            escucha(evento)
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


    def salaChat(self,sala):
        msg="CREATEROOM "+sala
        self.sock.send(msg.encode())

    def unirse(self,sala):
        msg="JOINROOM "+sala
        self.sock.send(msg.encode())

    def enviaSala(self,arr):
        msg="ROOMESSAGE"
        for s in arr:
            msg+=" "+s
        self.sock.send(msg.encode())

    def enviaPrivado(self,mensaje):
        msg="MESSAGE "+ mensaje
        msg=msg.replace("-r","")
        self.sock.send(msg.encode())
if __name__ == "__main__":
        port=int(input("Introduce el puerto:\n"))
        serv=Cliente('187.207.46.196',port,"")
        serv.seConecto()
        serv.enviado()
