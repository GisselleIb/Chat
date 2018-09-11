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
        self.privado=False
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
            print("Bienvenido, escribe -ayuda para ver "+
            "todos los comandos disponibles")
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
                    self.comandos(mensaje)
        self.sock.close()
        sys.exit()

    def ayuda(self):
        print(" -r + Usuario : Envía un mensaje privado al usuario especificado"+
        "\n -cierra : Cierra la sesión" +
        "\n -agrega + usuario: Agrega el usuario especificado a"+
        " la lista de contactos" +
        "\n -elimina + usuario: Elimina al usuario especificado" +
        "\n -sala + nombre de la sala: Ingresa a la sala de chat especificada" +
         "o la crea si no existe")

    def comandos(self,mensaje):
        men=mensaje.split()
        if(men[0] == "-p"):
            self.enviaPrivado(men)
        elif(men[0] == "-ayuda"):
            self.ayuda()
        elif(men[0] == "-cierra"):
            self.desconectado()
        elif(men[0] == "-agrega"):
            try:
                self.user.agregaContacto(men[1])
            except IndexError:
                print("Escribe el nombre de usuario")
        elif(men[0] == "-elimina"):
            try:
                self.user.eliminaContacto(men[1])
            except IndexError:
                print("Escribe el nombre del usuario que quieras eliminar")
        elif(men[0] == "-sala"):
            try:
                self.salaChat(men[1])
            except IndexError:
                print("Escribe un nombre para la sala")
        else:
            self.enviaTodos(mensaje)

    def enviaTodos(self,mensaje):
        msg=self.user.nombre +":"+mensaje
        self.sock.send(msg.encode())
        sys.stdout.write("<TU>")
        sys.stdout.write(mensaje)

    def salaChat(self,sala):
        msg="Sala: "+sala
        self.sock.send(msg.encode())

    def enviaPrivado(self,mensaje):
        for string in mensaje:
            if(string in self.user.directorio):
                self.sock.send(self.user.directorio[string].encode())
