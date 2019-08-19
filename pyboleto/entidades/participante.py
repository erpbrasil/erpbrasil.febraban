# -*- coding: utf-8 -*-


class Participante(object):
    def __init__(self, **kwargs):
        self.bairro = kwargs.pop('bairro', '')
        self.cep = kwargs.pop('cep', '')
        self.cidade = kwargs.pop('cidade', '')
        self.cnpj_cpf = kwargs.pop('cnpj_cpf', '')
        self.complemento = kwargs.pop('complemento', '')
        self.email = kwargs.pop('email', '')
        self.endereco = kwargs.pop('endereco', '')
        self.estado = kwargs.pop('estado', '')
        self.fone = kwargs.pop('fone', '')
        self.nome = kwargs.pop('nome', '')
        self.numero = kwargs.pop('numero', '')
