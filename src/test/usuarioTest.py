import unittest
import sys
sys.path.append('../..')
from src.usuario import Usuario
class UsuarioTest(unittest.TestCase):
    usuario=Usuario("name")
    def test_getNombre(self):
        self.assertEqual(self.usuario.getNombre(),"name")

    def test_setNombre(self):
        self.assertEqual(self.usuario.getNombre(),"name")
        self.usuario.setNombre("nombre")
        self.assertEqual(self.usuario.getNombre(),"nombre")
        self.usuario.setNombre("name")

    def test_agregaContacto(self):
        self.assertEqual(self.usuario.agregaContacto(None),
        "Inserte un contacto válido")
        self.usuario.agregaContacto("nombre")
        self.assertTrue("nombre" in self.usuario.directorio)

    def test_eliminaContacto(self):
        self.usuario.agregaContacto("N")
        self.assertTrue("N" in self.usuario.directorio)
        self.usuario.eliminaContacto("N")
        self.assertFalse("N" in self.usuario.directorio)
