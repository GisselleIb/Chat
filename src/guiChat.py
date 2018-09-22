# -*- coding: utf-8 -*-
import sys
from vista import Vista
from PyQt5 import QtCore, QtGui, QtWidgets

class GUIChat(QtWidgets.QMainWindow):
    """Clase que es la ventana principal de la interfaz gráfica
    """

    def __init__(self,controlador,cliente):
        """Constructor de la Clase
        Parámetros
        ----------
        controlador : Controlador
            Instancia de la clase controlador
        cliente : Cliente
            Instancia de la clase controlador
        """
        super(GUIChat, self).__init__()
        self.controlador=controlador
        self.cliente=cliente
        self.ui= Vista()
        self.ui.setupUi(self)
        self.ui.enviar.clicked.connect(self.enviaMensaje)
        self.cliente.escuchas.append(self.recibido)

    def enviaMensaje(self):
        """Método conectado al boton de enviar, envía una
        string al controlador para que se la pase al cliente
        """
        s=self.ui.entrada.text()
        self.ui.pantalla.append(s)
        self.ui.entrada.clear()
        self.controlador.actualizaCliente(s)

    def creaSala(self,evento):
        pass
    def status(self,evento):
        pass
    def unirseSala(self,evento):
        pass
    def recibido(self,mensaje):
        """Método que actualiza la interfaz
        Parámetros
        ----------
        mensaje : str
            Mensaje recibido del cliente para actualizar la interfaz
        """
        self.ui.pantalla.append(mensaje)
