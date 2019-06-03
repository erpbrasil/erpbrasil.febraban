# -*- coding: utf-8 -*-

class Cnab240Error(Exception):
    """Excessao base para o CNAB 240"""


class AtribuicaoCampoError(Cnab240Error): 
    """Tentativa de atribuicao de valor indevido ao campo""" 

    def __init__(self, campo, valor):
        self.campo = campo
        self.valor = valor
        super(AtribuicaoCampoError, self).__init__(self)
        
    def __unicode__(self):                
        return u'campo:{0} formato:{1} decimais:{2} digitos:{3} - valor:{4}'.\
            format( 
                self.campo.nome,    
                self.campo.formato, 
                self.campo.decimais,
                self.campo.digitos, 
                repr(self.valor),
            )


class NumDigitosExcedidoError(AtribuicaoCampoError):                             
    """Tentativa de atribuicao de valor mais longo que o campo suportaia"""      
                                                                                 

class TipoError(AtribuicaoCampoError):                                           
    """Tentativa de atribuicao de tipo nao suportado pelo campo"""


class NumDecimaisError(AtribuicaoCampoError):
    """Numero de casasa decimais em desacordo com especificacao"""


class FaltandoArgsError(Exception):
    """Faltando argumentos na chamada do metodo"""

    def __init__(self, args_faltantes):
        self.args_faltantes = args_faltantes
        super(FaltandoArgsError, self).__init__(self)

    def __unicode__(self):
        return (u'Os seguintes kwargs sao obrigatorios e nao foram '
                u'encontrados: {0}').format(', '.join(self.args_faltantes))


class NenhumLoteError(Exception):
    """Tentativa de escrita de arquivo sem lotes."""


class NenhumEventoError(Exception):
    """Tentativa de escrita de lote sem eventos. """


