# -*- coding: utf-8 -*-

from erpbrasil.febraban.boleto.custom_property import CustomProperty
from erpbrasil.febraban.entidades import Boleto


class BancoInter(Boleto):
    """ Implementa a Api do BancoInter """

    seu_numero = CustomProperty('seu_numero', 15)
    nosso_numero = CustomProperty('nosso_numero', 11)
    linha_digitavel = None
    barcode = None
    _gera_pdf = False

    @classmethod
    def convert_to(cls, obj, **kwargs):
        obj.__class__ = cls
        obj.__special_init__()
        for key, value in kwargs.items():
            if hasattr(obj, key):
                obj.__dict__[key] = value

    def __init__(self, **kwargs):
        super(BancoInter, self).__init__(**kwargs)
        self.codigo_banco = "077"
        self.sacado_complemento = kwargs.pop('sacado_complemento', "")
        self.sacado_numero = kwargs.pop('sacado_numero', "")
        self.sacado_ddd = kwargs.pop('sacado_ddd', "")
        self.sacado_telefone = kwargs.pop('sacado_telefone', "")
        self.sacado_bairro = kwargs.pop('sacado_bairro', "")
        self.sacado_email = kwargs.pop('sacado_email', "")
        self.mora = dict(
            codigoMora="ISENTO",
            valor=0,
            taxa=0
        )
        self.multa = dict(
            codigoMulta="NAOTEMMULTA",
            valor=0,
            taxa=0
        )

    def _emissao_data(self):
        pagador= dict(
            cnpjCpf=self.sacado_documento,
            nome=self.sacado_nome,
            email=self.sacado_email,
            telefone=self.sacado_telefone,
            cep=self.sacado_cep,
            numero=self.sacado_numero,
            complemento=self.sacado_complemento,
            bairro=self.sacado_bairro,
            cidade=self.sacado_cidade,
            uf=self.sacado_uf,
            endereco=self.sacado_endereco,
            ddd=self.sacado_ddd,
            tipoPessoa=self.sacado_tipo_pessoa,
        )
        mensagem1=dict(
           {'linha{}'.format(k+1):v for (k,v) in enumerate(self._instrucoes)}
        )
        desconto1=dict(
            codigoDesconto="NAOTEMDESCONTO",
            taxa=0,
            valor=0,
            data=""
        )
        desconto2=dict(
            codigoDesconto="NAOTEMDESCONTO",
            taxa=0,
            valor=0,
            data=""
        )
        desconto3=dict(
            codigoDesconto="NAOTEMDESCONTO",
            taxa=0,
            valor=0,
            data=""
        )
        data = dict(
            pagador=pagador,
            dataEmissao=self.data_documento,
            seuNumero=self.numero_documento,
            dataLimite="SESSENTA",
            dataVencimento=self.data_documento,
            mensagem=mensagem1,
            desconto1=desconto1,
            desconto2=desconto2,
            desconto3=desconto3,
            valorNominal=self.valor_documento,
            valorAbatimento=0,
            multa=self.multa,
            mora=self.mora,
            cnpjCPFBeneficiario = self.cedente_documento,
            numDiasAgenda="SESSENTA"
        )
        return data
