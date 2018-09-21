from servidor import Servidor
from controlador import Controlador
from usuario import Usuario
from cliente import Cliente
from guiChat import GUIChat
from PyQt5 import QtWidgets
import threading
import time
import sys
class Chat(QtWidgets.QApplication):
    def __init__(self,sys_argv,port):
        super(Chat,self).__init__(sys_argv)
        self.cliente=Cliente('0.0.0.0',port)
        self.controlador=Controlador(self.cliente)
        self.igchat=GUIChat(self.controlador,self.cliente)
        self.cliente.seConecto()
        t1=threading.Thread(target=self.cliente.enviado)
        t1.setDaemon(True)
        t1.start()
        time.sleep(0.001)
        self.igchat.show()


if __name__ == "__main__":
    port=int(input("Introduce el puerto:\n"))
    app=Chat(sys.argv,port)
    sys.exit(app.exec_())
