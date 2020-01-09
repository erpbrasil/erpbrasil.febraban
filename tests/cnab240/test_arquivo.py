
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os
import codecs

from erpbrasil.febraban.cnab240 import errors
from erpbrasil.febraban.cnab240.bancos import itau
from erpbrasil.febraban.cnab240.tipos import Arquivo
from .data import get_itau_data_from_dict, get_itau_file_remessa, \
                                                                ARQS_DIRPATH


class TestCnab240(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCnab240, self).__init__(*args, **kwargs)
        self.maxDiff = None

    def setUp(self):
        self.itau_data = get_itau_data_from_dict()
        self.arquivo = Arquivo(itau, **self.itau_data['arquivo'])

    def test_unicode(self):
        self.arquivo.incluir_cobranca(**self.itau_data['cobranca'])
        self.assertEqual(unicode(self.arquivo), get_itau_file_remessa())

    def test_empty_data(self):
        arquivo = Arquivo(itau)
        self.assertRaises(errors.ArquivoVazioError, unicode, arquivo)

    def test_leitura(self):
        return_file_path = os.path.join(ARQS_DIRPATH, 'cobranca.itau.ret')
        ret_file = codecs.open(return_file_path, encoding='ascii')
        arquivo = Arquivo(itau, arquivo=ret_file)
        ret_file.seek(0)
        self.assertEqual(ret_file.read(), unicode(arquivo))

if __name__ == '__main__':
    unittest.main()
