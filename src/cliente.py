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
        host : str
           La dirección IP del cliente.
        port : int
           El puerto del cliente.
        user : Usuario
           Clase que guardara los datos del usuario.
        escuchas : [func]
           Lista de escuchas
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

    def seConecto(self):
        """Conecta el cliente con el Servidor.
        """
        try:
            self.sock.connect((self.host,self.port))
            self.actualiza("Bienvenido,para poder enviar mensajes "+
            "identificate con tu nombre de usuario con el comando -id nombre.\n"+
             "Escribe -help para ver mas comandos")
            return True
        except socket.timeout:
            return False

    def desconectado(self):
        """ Desconecta el socket y cierra el cliente.
        """
        d="DISCONNECT"
        self.sock.send(d.encode())
        sys.exit()
        self.sock.close()

    def enviado(self):
        """Checa cuando llega el mensaje de otro cliente
        y lo recibe.
        """
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
        """Imprime un menu de ayuda con los comandos que se pueden
        utilizar en el chat.
        """
        s=" -r usuario mensaje: Envía un mensaje privado al usuario especificado"+ \
        "\n -d : Cierra la sesión" +\
        "\n -s sala: Crea una nueva sala de chat con el nombre especificado" +\
         "\n -y sala: Te unes a la sala de chat especificada, pero tienes"+\
         "\n que haber sido invitado primero"+\
         "\n -u : Enseña todos los usuarios conectados y sus estados"+\
         "\n -rm mensaje : Envía un mensaje a la sala especificada"+\
         "\n -st status : Cambia tu status por el especificado"+\
         "\n -i sala usuario1 usuario2...:Invita a los usuarios especificados a "+\
         "la sala especificada"
        self.actualiza(s)

    def comandos(self,mensaje):
        """Revisa que comando contiene el mensaje escrito por el usuario.
        Parámetros
        ---------
        mensaje : str
           Mensaje escrito por el usuario.
        """
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
        """Actualiza el estado de la interfaz
        Parámetros
        ----------
        evento : str
            String que se pasa al escucha que modificara
            la interfaz.
        """
        for escucha in self.escuchas:
            escucha(evento)

    def status(self):
        """Manda al servidor un mensaje para cambiar
        el status del usuario.
        """
        msg="STATUS"
        self.sock.send(msg.encode())

    def identifica(self,nombre):
        """Manda al servidor un mensaje para identificar
        al usuario
        Parámetros
        ----------
        nombre : str
           Nombre del usuario
        """
        id="IDENTIFY "+nombre
        self.user.nombre=nombre
        self.sock.send(id.encode())

    def invita(self,l):
        """ Manda un mensaje al servidor con la sala
        e invitados
        Parámetros
        ----------
        l : [str]
           Lista con el nombre de la sala y los nombres
           de los usuarios invitados
        """
        msg="INVITE"
        for usuario in l:
            msg+=" "+usuario
        self.sock.send(msg.encode())

    def showUsuarios(self):
        """Manda al servidor un mensaje para saber
        quienes son los usuarios conectados
        """
        msg="USERS"
        self.sock.send(msg.encode())

    def enviaTodos(self,mensaje):
        """Manda al servidor un mensaje que debe ser
        transmitido a todos los usuarios conectados
        Parámetros
        ----------
        mensaje : str
           Mensaje público
        """
        msg="PUBLICMESSAGE "+ mensaje
        self.sock.send(msg.encode())

    def salaChat(self,sala):
        """Manda al servidor un mensaje con el nombre
        de una sala para que esta sea creada
        Parámetros
        ----------
        sala : str
           Nombre de la sala a crear.
        """
        msg="CREATEROOM "+sala
        self.sock.send(msg.encode())

    def unirse(self,sala):
        """Manda al servidor un mensaje con el nombre de
        la sala a la que se quiere unir
        Parámetros
        ----------
        sala : str
           Nombre de la sala.
        """
        msg="JOINROOM "+sala
        self.sock.send(msg.encode())

    def enviaSala(self,arr):
        """Manda un mensaje al servidor que deberá ser
        transmitido a todos los usuarios de la sala indicada
        Parámetros
        ----------
        arr : [str]
           Lista de strings que contiene el nombre de la
           sala y el mensaje.
        """
        msg="ROOMESSAGE"
        for s in arr:
            msg+=" "+s
        self.sock.send(msg.encode())

    def enviaPrivado(self,mensaje):
        """Manda un mensaje al servidor que deberá ser transmitido
        solo a una persona indicada por el usuario
        Parámetros
        ----------
        mensaje : str
           Mensaje a enviar.
        """
        msg="MESSAGE "+ mensaje
        msg=msg.replace("-r","")
        self.sock.send(msg.encode())
        
if __name__ == "__main__":
        port=int(input("Introduce el puerto:\n"))
        serv=Cliente('187.207.46.196',port,"")
        serv.seConecto()
        serv.enviado()
