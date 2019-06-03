# -*- coding: utf-8 -*-

"""
    pyboleto.base
    ~~~~~~~~~~~~~

    Base para criação dos módulos dos bancos. Comtém funções genéricas
    relacionadas a geração dos dados necessários para o boleto bancário.

    :copyright: © 2011 - 2012 by Eduardo Cereto Carvalho
    :license: BSD, see LICENSE for more details.

"""


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
