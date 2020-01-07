# -*- coding: utf-8 -*-


class BoletoException(Exception):
    """ Exceções para erros no pyboleto"""
    def __init__(self, message):
        Exception.__init__(self, message)
