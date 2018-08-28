import sys
import unittest
import socket
sys.path.append('../..')
from src.servidor import Servidor
class ServidorTest(unittest.TestCase):

    def test_conectaCliente(self):
        serv=Servidor('',68)
        self.assertFalse(serv.conectaCliente())
        serv.setHost('')
        serv.setPort(80)
        self.assertTrue(serv.conectaCliente())

    def test_getHost(self):
        serv=Servidor('',80)
        self.assertEqual(serv.getHost(),'')

    def test_getPort(self):
        serv=Servidor('',80)
        self.assertEqual(serv.getPort(),80)

    def test_setHost(self):
        serv=Servidor('',80)
        self.assertEqual(serv.getHost(),'')
        serv.setHost(socket.gethostname())
        self.assertEqual(socket.gethostname(),serv.getHost())

    def test_setPort(self):
        serv=Servidor('',80)
        self.assertEqual(serv.getPort(),80)
        serv.setPort(8888)
        self.assertEqual(serv.getPort(),8888)


if __name__ == '__main__':
    unittest.main()
