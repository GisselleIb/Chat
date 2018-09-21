# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vista.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!
import sys
from vista import Vista
from PyQt5 import QtCore, QtGui, QtWidgets

class GUIChat(QtWidgets.QMainWindow):

    def __init__(self,controlador,cliente):
        super(GUIChat, self).__init__()
        self.controlador=controlador
        self.cliente=cliente
        self.ui= Vista()
        self.ui.setupUi(self)
        self.ui.enviar.clicked.connect(self.enviaMensaje)
        self.cliente.escuchas.append(self.recibido)

    def enviaMensaje(self):
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
        self.ui.pantalla.append(mensaje)
