
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from erpbrasil.febraban.cnab.bancos import itau
from erpbrasil.febraban.cnab.tipos import Evento
from .data import get_itau_data_from_file

import sys
PY3 = sys.version_info[0] == 3

if PY3:
    unicode = str


class TestEvento(unittest.TestCase):
    def setUp(self):
        self.evento = Evento(itau, 1)

    def test_getattributes(self):
        self.assertEqual(self.evento._segmentos, [])

        test_obj = type('TestObject', (object,), {'test_attr': None})()
        self.evento._segmentos.append(test_obj)
        test_obj.test_attr = 'Hello World'
        self.evento.test_attr = 'Goodbye World'

        self.assertNotEqual(self.evento.test_attr, 'Goodbye World')
        self.assertEqual(self.evento.test_attr, 'Hello World')

    def test_unicode(self):
        self.assertEqual(unicode(self.evento), u'')
        self.evento._segmentos.append('test_1')
        self.assertEqual(unicode(self.evento), u'test_1')
        self.evento._segmentos.append('test_2')
        self.assertEqual(unicode(self.evento), u'test_1\r\ntest_2')

