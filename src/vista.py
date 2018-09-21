# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vista.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
#from cliente import Cliente
class Vista(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setAccessibleName("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pantalla = QtWidgets.QTextBrowser(self.centralwidget)
        self.pantalla.setObjectName("pantalla")
        self.gridLayout.addWidget(self.pantalla, 0, 0, 1, 2)
        self.entrada = QtWidgets.QLineEdit(self.centralwidget)
        self.entrada.setObjectName("entrada")
        self.gridLayout.addWidget(self.entrada, 1, 0, 1, 1)
        self.enviar = QtWidgets.QPushButton(self.centralwidget)
        self.enviar.setObjectName("enviar")
        self.gridLayout.addWidget(self.enviar, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")
        self.menuStatus = QtWidgets.QMenu(self.menubar)
        self.menuStatus.setObjectName("menuStatus")
        self.menuSalas = QtWidgets.QMenu(self.menubar)
        self.menuSalas.setObjectName("menuSalas")
        MainWindow.setMenuBar(self.menubar)
        self.actionActivo = QtWidgets.QAction(MainWindow)
        self.actionActivo.setObjectName("actionActivo")
        self.actionOcupado = QtWidgets.QAction(MainWindow)
        self.actionOcupado.setObjectName("actionOcupado")
        self.actionAusente = QtWidgets.QAction(MainWindow)
        self.actionAusente.setObjectName("actionAusente")
        self.creaSalas = QtWidgets.QAction(MainWindow)
        self.creaSalas.setObjectName("creaSalas")
        self.actionUnirse_a_sala = QtWidgets.QAction(MainWindow)
        self.actionUnirse_a_sala.setObjectName("actionUnirse_a_sala")
        self.menuStatus.addSeparator()
        self.menuStatus.addAction(self.actionActivo)
        self.menuStatus.addAction(self.actionOcupado)
        self.menuStatus.addAction(self.actionAusente)
        self.menuSalas.addAction(self.creaSalas)
        self.menuSalas.addAction(self.actionUnirse_a_sala)
        self.menubar.addAction(self.menuStatus.menuAction())
        self.menubar.addAction(self.menuSalas.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chat"))
        self.enviar.setText(_translate("MainWindow", "Enviar"))
        self.menuStatus.setTitle(_translate("MainWindow", "Status"))
        self.menuSalas.setTitle(_translate("MainWindow", "Salas"))
        self.actionActivo.setText(_translate("MainWindow", "Activo"))
        self.actionOcupado.setText(_translate("MainWindow", "Ocupado"))
        self.actionAusente.setText(_translate("MainWindow", "Ausente"))
        self.creaSalas.setText(_translate("MainWindow", "Crea sala"))
        self.actionUnirse_a_sala.setText(_translate("MainWindow", "Unirse a sala"))

    def enviaMensaje(self):
        self.enviar.clicked.connect(comando= lambda: self.pantalla.setText(self.entrada.text()))
        return self.pantalla.toPlainText()

    def creaSala(self,evento):
        pass
    def status(self,evento):
        pass
    def unirseSala(self,evento):
        pass
    def click(self):
        pass
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui =Vista()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
