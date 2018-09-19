import unittest
import sys
sys.path.append('../..')
from src.sala import Sala
class SalaTest(unittest.TestCase):
    sala=None
    def setUp(self):
        self.sala=Sala("chatroom","owner")
    def test_agregaInv(self):
        self.sala.agregaInv("name")
        self.assertTrue("name" in self.sala.invitados)
        self.assertFalse("n" in self.sala.invitados)

    def test_agrega(self):
        self.sala.agregaInv("name")
        self.sala.agregaInv("nom")
        self.sala.agrega("name")
        self.assertTrue("name" in self.sala.clientes)
        self.assertFalse("name" in self.sala.invitados)

    def test_elimina(self):
        self.sala.agregaInv("name")
        self.sala.agrega("name")
        self.sala.elimina("name")
        self.assertFalse("name" in self.sala.clientes)
