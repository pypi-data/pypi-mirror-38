import unittest
from comentariosemol import limitar, nombrar
from urllib.parse import urlparse
import os
from freezegun import freeze_time
from datetime import datetime

class test_limitar(unittest.TestCase):
    def test_limitar_numero_menor_a_lista(self):
        lista = [1, 2, 3, 4, 5, 6, 7]
        numero = 5
        limitar(lista, numero)
        self.assertEqual(lista, [1, 2, 3, 4, 5])

    def test_limitar_lista_con_unico_elemento(self):
        lista = 2
        numero = 3
        lista = limitar(lista, numero)
        self.assertEqual(lista, [2])

    def test_limitar_numero_mayor_a_lista(self):
        lista = [1, 2, 3, 4, 5, 6, 7]
        numero = 8
        limitar(lista, numero)
        self.assertEqual(lista, [1, 2, 3, 4, 5, 6, 7])

    def test_limitar_numero_igual_a_lista(self):
        lista = [1, 2, 3, 4, 5, 6, 7]
        numero = 7
        limitar(lista, numero)
        self.assertEqual(lista, [1, 2, 3, 4, 5, 6, 7])

class test_nombrar(unittest.TestCase):
    @freeze_time("2018-11-03 19:05:00")
    def test_nombrar_csv(self):
        url = urlparse('https://www.emol.com/noticias/Nacional/2018/11/03/926164/Embajada-de-Francia-en-Chile-se-desmarca-del-otorgamiento-de-asilo-a-Palma-Salamanca.html')
        filepath = '/home/testing'
        nombre_archivo = nombrar(filepath, url)
        self.assertEqual(nombre_archivo, '/home/testing/emolEmbajada-de-Francia-en-Chile-se-desmarca3-11_19-5.csv')
