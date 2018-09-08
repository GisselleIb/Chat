import unittest
import sys
import socket
sys.path.append('../..')
from src.cliente import Cliente
class ClienteTest(unittest.TestCase):

    def test_seConecto(self):
        client=Cliente(socket.gethostname(),65)
        self.assertFalse(client.seConecto())
        client.setPort(socket.gethostname())
        self.assertTrue(client.seConecto())

    def test_desconectado(self):
        self.assertEqual("Desconectando del servidor",client.desconectado())

    def test_enviado(self):
        client=Cliente(socket.gethostname(),60000)
        assertFalse(client.seConecto())


    def test_getHost(self):
        serv=Servidor('',59243)
        self.assertEqual(serv.getHost(),'')

    def test_getPort(self):
        serv=Servidor('',59243)
        self.assertEqual(serv.getPort(),59243)

    def test_setHost(self):
        serv=Servidor('',59243)
        self.assertEqual(serv.getHost(),'')
        serv.setHost(socket.gethostname())
        self.assertEqual(socket.gethostname(),serv.getHost())

    def test_setPort(self):
        serv=Servidor('',50000)
        self.assertEqual(serv.getPort(),59243)
        serv.setPort(8888)
        self.assertEqual(serv.getPort(),8888)

    def test_privado(self):
        m1="-r user"
        m2="user"
        self.assertTrue(client.privado(m1))
        self.assertFalse(client.privado(m2))

if __name__ == '__main__':
    unittest.main()
