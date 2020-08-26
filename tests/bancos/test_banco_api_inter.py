# -*- coding: utf-8 -*-
import os
import unittest

from erpbrasil.febraban.api.inter import ApiInter
from erpbrasil.febraban.boleto.banco.inter import BancoInter

from .testutils import BoletoTestCase


class TestBancoApiInter(BoletoTestCase):
    def setUp(self):
        certificado_cert = os.environ.get('certificado_inter_cert')
        certificado_key = os.environ.get('certificado_inter_key')
        self.api = ApiInter(
            cert=(certificado_cert, certificado_key),
            conta_corrente='14054310'
        )
        self.dados = []
        for i in range(3):
            d = BancoInter()
            d.cedente_documento = '23130935000198'
            d.data_documento = '2020-08-26'
            d.data_vencimento = '2020-08-28'
            d.numero_documento = str(456 + i)
            d.valor_documento = 100
            d.sacado_nome = "Sacado Teste"
            d.sacado_documento = "26103754097"
            d.sacado_cidade = "SAO PAULO"
            d.sacado_uf = "SP"
            d.sacado_complemento = "casa"
            d.sacado_endereco = "Rua dos TESTES"
            d.sacado_numero = "15"
            d.sacado_ddd = "12"
            d.sacado_telefone = "988763663"
            d.sacado_bairro = "CENTRO"
            d.sacado_cep = "31327130"
            d.sacado_email = "test@example.com"
            d.sacado_tipo_pessoa = "FISICA"
            d.instrucoes = [
                'TESTE 1',
                'TESTE 2',
                'TESTE 3',
                'TESTE 4',
            ]
            self.dados.append(d)

    def test_data(self):
        for item in self.dados:
            self.assertTrue(item._emissao_data())

    def test_boleto_api(self):
        for item in self.dados:
            resposta = self.api.boleto_inclui(item._emissao_data())
            item.nosso_numero = resposta['nossoNumero']
            item.seu_numero = resposta['seuNumero']
            item.linha_digitavel = resposta['linhaDigitavel']
            item.barcode = resposta['codigoBarras']

            self.assertListEqual(
                list(resposta.keys()),
                ['seuNumero', 'nossoNumero', 'codigoBarras', 'linhaDigitavel'],
                'Erro ao registrar boleto'
            )

        resposta = self.api.boleto_consulta(
            data_inicial='2020-01-01', data_final='2020-12-01',
            ordenar_por='SEUNUMERO'
        )
        self.assertTrue(resposta, 'Falha ao consultar boletos')

        for item in self.dados:
            resposta = self.api.boleto_pdf(nosso_numero=item.nosso_numero)
            self.assertTrue(resposta, 'Falha ao imprimir boleto')

        for item in self.dados:
            resposta = self.api.boleto_baixa(
                nosso_numero=item.nosso_numero,
                codigo_baixa='SUBISTITUICAO',
            )
            self.assertTrue(resposta, 'Falha ao Baixar boletos')


suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoApiInter)

if __name__ == '__main__':
    unittest.main()
