# -*- coding: utf-8 -*-

"""
    pyboleto.base
    ~~~~~~~~~~~~~

    Base para criação dos módulos dos bancos. Comtém funções genéricas
    relacionadas a geração dos dados necessários para o boleto bancário.

    :copyright: © 2011 - 2012 by Eduardo Cereto Carvalho
    :license: BSD, see LICENSE for more details.

"""

import re
import string


def modulo10(num):
    if not isinstance(num, str):
        raise TypeError
    soma = 0
    peso = 2
    for c in reversed(num):
        parcial = int(c) * peso
        if parcial > 9:
            s = str(parcial)
            parcial = int(s[0]) + int(s[1])
        soma += parcial
        if peso == 2:
            peso = 1
        else:
            peso = 2

    resto10 = soma % 10
    if resto10 == 0:
        result = 0
    else:
        result = 10 - resto10

    return result


def modulo11(num, base=9, r=0):
    if not isinstance(num, str):
        raise TypeError
    soma = 0
    fator = 2
    for c in reversed(num):
        soma += int(c) * fator
        if fator == base:
            fator = 1
        fator += 1
    if r == 0:
        soma = soma * 10
        digito = soma % 11
        if digito == 10:
            digito = 0
        return digito
    if r == 1:
        resto = soma % 11
        return resto


def remove_pontuacao(string_value):
    return re.sub(
        '[%s]' % re.escape(string.punctuation), '', string_value or ''
    )


def formata_cpf_cnpj(cnpj_cpf):
    """
    >>> formata_cpf_cnpj(0)
    '000.000.000-00'

    >>> formata_cpf_cnpj('00.905.849/0002-95')
    '00.905.849/0002-95'
    
    >>> formata_cpf_cnpj('76.162.730/0001-50')
    '76.162.730/0001-50'
    
    >>> formata_cpf_cnpj('372.448.997-23')
    '372.448.997-23'
    
    >>> formata_cpf_cnpj('000.448.997-23')
    '000.448.997-23'
    
    >>> formata_cpf_cnpj('372.448.997-23')
    '000.148.997-23'
    """

    if cnpj_cpf:
        val = re.sub('[^0-9]', '', cnpj_cpf)
        val = val.lstrip("0")
        if len(val) <= 11:
            val = val.zfill(11)
            return "%s.%s.%s-%s" % (
                val[0:3], val[3:6], val[6:9], val[9:11])
        elif 11 < len(val) <= 14:
            val = val.zfill(14)
            return "%s.%s.%s/%s-%s" % (
                val[0:2], val[2:5], val[5:8], val[8:12], val[12:14])
