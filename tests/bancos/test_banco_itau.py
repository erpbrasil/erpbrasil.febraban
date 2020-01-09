# -*- coding: utf-8 -*-
import unittest
import datetime

from erpbrasil.febraban.bank.itau import BoletoItau
from erpbrasil.febraban.cnab240.tipos import ArquivoCobranca400
from erpbrasil.febraban.cnab240.bancos import itau_cobranca_400

from .testutils import BoletoTestCase


class TestBancoItau(BoletoTestCase):
    def setUp(self):
        self.dados = []
        for i in range(3):
            d = BoletoItau()
            d.carteira = '109'
            d.agencia_cedente = '0293'
            d.conta_cedente = '01328'
            d.data_vencimento = datetime.date(2009, 10, 19)
            d.data_documento = datetime.date(2009, 10, 19)
            d.data_processamento = datetime.date(2009, 10, 19)
            d.valor_documento = 29.80
            d.nosso_numero = str(157 + i)
            d.numero_documento = str(456 + i)
            self.dados.append(d)

    def test_linha_digitavel(self):
        self.assertEqual(
            self.dados[0].linha_digitavel,
            '34191.09008 00015.710296 30132.800001 9 43950000002980'
        )

    def test_codigo_de_barras(self):
        self.assertEqual(
            self.dados[0].barcode,
            '34199439500000029801090000015710293013280000'
        )

    def test_agencia(self):
        self.assertEqual(self.dados[0].agencia_cedente, '0293')

    def test_conta(self):
        self.assertEqual(self.dados[0].conta_cedente, '01328')

    def test_dv_nosso_numero(self):
        self.assertEqual(self.dados[0].dv_nosso_numero, 1)

    def test_dv_agencia_conta_cedente(self):
        self.assertEqual(self.dados[0].dv_agencia_conta_cedente, 0)

    def test_cnab400(self):
        arquivo = ArquivoCobranca400(banco=itau_cobranca_400)
        for id, boleto in enumerate(self.dados):
            boleto_dict = {}
            for key, val in boleto.__dict__.items():
                boleto_dict.update({key: val})

            arquivo.incluir_cobranca(**boleto_dict)
            arquivo.trailer.num_seq_registro = id+1
        print(arquivo.exportar())

suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoItau)

if __name__ == '__main__':
    unittest.main()
