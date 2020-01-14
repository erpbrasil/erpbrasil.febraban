# -*- coding: utf-8 -*-

from ..exceptions import BoletoException
BANCOS_IMPLEMENTADOS = {
    '001': 'bancodobrasil.BoletoBB',
    '041': 'banrisul.BoletoBanrisul',
    '237': 'bradesco.BoletoBradesco',
    '104': 'caixa.BoletoCaixa',
    '399': 'hsbc.BoletoHsbc',
    '341': 'itau.BoletoItau',
    '356': 'real.BoletoReal',
    '033': 'santander.BoletoSantander',
    '748': 'sicredi.BoletoSicredi',
}


def get_class_for_codigo(banco_codigo):
    """Retorna a classe que implementa o banco

    :param banco_codigo:
    :type banco_codigo: string
    :return: Classo do Banco subclasse de :class:`pyboleto.data.Boleto`
    :rtype: :class:`pyboleto.data.Boleto`
    """
    try:
        banco = BANCOS_IMPLEMENTADOS[banco_codigo].split('.')
    except KeyError:
        raise(BoletoException('Este banco não é suportado.'))

    mod = __import__('erpbrasil.febraban.boleto.banco.' + banco[0],
                     globals(), locals(), [banco[1]])

    return getattr(mod, banco[1])
