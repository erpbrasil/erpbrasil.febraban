# -*- coding: utf-8 -*-
from erpbrasil.febraban.bank.itau import BoletoItau

import json
import requests
import sys

PY3 = sys.version_info[0] == 3

if PY3:
    unicode = str


def limpa_formatacao(cnpj_cpf):
    """
    Limpa os caracteres de formatação
    :param cnpj_cpf: CPF ou CNPJ de entrada
    :return: Retorna o CPF ou CNPJ sem formatação
    """
    return ''.join([c for c in cnpj_cpf if c.isdigit()])


def truncate_str(_entry_str, _len):
    """
    Método para limitar o tamanho das strings utilizadas na classe
    :param _entry_str: string de entrada
    :param _len: o tamanho limite do retorno
    :return: A string _entry_str limitada pelo tamanho _len1
    """
    if isinstance(_entry_str, str) or isinstance(_entry_str, unicode):
        return _entry_str[:_len]
    return ""


class ApiItau(BoletoItau):
    """ Implementa a Api do Itaú

        A partir dos dados fornecidos pelo Boleto do Itaú é feita a conexão
        com o próprio Itaú para o registro de faturas.
    """

    @classmethod
    def convert_to(cls, obj, **kwargs):
        obj.__class__ = cls
        obj.__special_init__()
        for key, value in kwargs.items():
            if hasattr(obj, key):
                obj.__dict__[key] = value

    def __init__(self):
        super(ApiItau, self).__init__()
        self.__special_init__()

    def __special_init__(self):
        self.tipo_ambiente = '1'
        # 1 - HML
        # 2 - PROD

        self.tipo_cobranca = '1'
        # Para boletos 1
        # Para debito automático 2
        # Para cartão de crédito 3
        # Para TEF reversa 4

        self.tipo_registro = '1'
        # Para registro 1
        # Para alteração 2
        # Para consulta 3

        self.tipo_produto = '00006'
        self.subproduto = '00008'
        self.titulo_aceite = 'S'
        # Se for um boleto de cobrança * “S”
        # Se for um boleto de proposta * “N”

        self.codigo_moeda_cnab = '09'
        # Deve ser informado o código CNAB da moeda que expressa o valor do
        # título. Para o Banco Itaú é sempre emitido em Real.
        # Para moeda real o campo deve ser preenchido com 09.

        self.tipo_pagamento = 3
        # Pagamento realizado à vista * 1
        # Pagamento com data de vencimento determinada * 3

        # Pagamentos com Tipo de Pagamento à vista não precisam preencher o
        # parâmetro data_vencimento

        self.indicador_pagamento_parcial = False
        # Aceita pagamento parcial - true
        # Não aceita pagamento parcial - false

        self.tipo_juros = 5
        # Valor diário para incidência de juros após um dia corrido da Data de
        # Vencimento - 1

        # Percentual diário para incidência de juros após um dia corrido da
        # Data de Vencimento  - 2

        # Percentual mensal para incidência de juros após um dia corrido da
        # Data de Vencimento - 3

        # Percentual anual para incidência de juros após um dia corrido da
        # Data de Vencimento - 4

        # Não se aplica juros caso o título seja pago após a Data de
        # Vencimento (isento)  - 5

        # Valor diário para incidência de juros após um dia útil da Data de
        # Vencimento - 6

        # Percentual diário para incidência de juros após um dia útil da Data
        # de Vencimento - 7

        # Percentual mensal para incidência de juros após um dia útil da Data
        # de Vencimento - 8

        # Percentual anual para incidência de juros após um dia útil da Data de
        # Vencimento - 9

        self.tipo_multa = 3
        # Quando se deseja cobrar um valor fixo de multa após o vencimento. - 1

        # Quando se deseja cobrar um percentual do valor do título de multa
        # após o vencimento. - 2

        # Quando não se deseja cobrar multa caso o pagamento seja feito após o
        # vencimento (isento) - 3

        self.tipo_desconto = '0'
        # Quando não houver condição de desconto – sem desconto 0
        # Quando o desconto for um valor fixo se o título for pago até a data
        # informada (data_desconto) - 1

        # Quando o desconto for um percentual do valor do título e for pago
        # até a data informada (data_desconto) - 2

        # Quando o desconto for um valor dependente da quantidade de
        # dias corridos na antecipação do pagamento referente à Data de
        # Vencimento. - 3

        # Quando o desconto for um valor dependente da quantidade de
        # dias úteis na antecipação do pagamento referente à Data de
        # Vencimento. - 4

        # Quando o desconto for um percentual do valor do título e
        # dependente da quantidade de dias corridos na antecipação do
        # pagamento referente à Data de Vencimento - 5

        # Quando o desconto for um percentual do valor do título e
        # dependente da quantidade de dias úteis na antecipação do
        # pagamento referente à Data de Vencimento. - 6

        self.tipo_autorizacao_recebimento = '3'
        # Quando o título aceita qualquer valor divergente ao da cobrança - 1

        # Quando o título contém uma faixa de valores aceitos para recebimentos
        # divergentes - 2

        # Quando o título não deve aceitar pagamentos de valores divergentes
        # ao da cobrança - 3

        # Quando o título aceitar pagamentos de valores superiores ao mínimo
        # definido - 4

        self.especie = '08'
        # Duplicata Mercantil 01
        # Nota Promissória 02
        # Nota de Seguro 03
        # Mensalidade Escolar 04
        # Recibo 05
        # Contrato 06
        # Cosseguros 07
        # Duplicata de Serviço 08
        # Letra de Câmbio 09
        # Nota de Débitos 13
        # Documento de Dívida 15
        # Encargos Condominiais 16

    def post(self, token, itau_key, endpoint):
        data = self._generate_data()
        json_data = json.dumps(data)

        headers = {
            'access_token': token,  # Access-Token retornado pelo api_validation()
            'itau-chave': itau_key,
            'accept': "application/vnd.itau",
            'cache-control': "no-cache",
            'identificador':
                limpa_formatacao(self.cedente_documento).zfill(14),
        }
        # operation_id = self.operation_ids.create({})
        # request = operation_id.post(
        #     url=RAIZ_ENDPOINT,
        #     data=json_data,
        #     headers=headers
        # )

        request = requests.post(
            url=endpoint,
            data=json_data,
            headers=headers
        )

        return request

    @staticmethod
    def generate_api_key(client_id, client_secret, endpoint):

        params = dict(
            scope='readonly',
            grant_type='client_credentials',
            client_id=client_id,
            client_secret=client_secret
        )

        request = requests.post(
            url=endpoint,
            data=params,
        )

        return request

    def _generate_data(self):
        data = dict(
            tipo_ambiente=int(self.tipo_ambiente),
            tipo_registro=int(self.tipo_registro),
            tipo_cobranca=int(self.tipo_cobranca),
            tipo_produto=self.tipo_produto,
            subproduto=self.subproduto,

            beneficiario=dict(
                cpf_cnpj_beneficiario=limpa_formatacao(self.cedente_documento),
                agencia_beneficiario=self.agencia_cedente,
                conta_beneficiario=self.conta_cedente.zfill(7),
                digito_verificador_conta_beneficiario=
                str(self.dv_agencia_conta_cedente),
            ),

            identificador_titulo_empresa=truncate_str(
                self.cedente.rjust(25, ' '), 25),

            pagador=dict(
                cpf_cnpj_pagador=limpa_formatacao(self.sacado_documento),
                nome_pagador=truncate_str(self.sacado_nome.rjust(30, ' '), 30),
                logradouro_pagador=truncate_str(self.sacado_endereco, 40),
                bairro_pagador=truncate_str(self.sacado_bairro, 15),
                cidade_pagador=truncate_str(self.sacado_cidade, 20),
                uf_pagador=truncate_str(self.sacado_uf, 2),
                cep_pagador=truncate_str(limpa_formatacao(self.sacado_cep), 8),
            ),

            # sacador_avalista=dict(
            #     cpf_cnpj_sacador_avalista=self.cpf_cnpj_sacador_avalista,
            #     nome_sacador_avalista=self.nome_sacador_avalista,
            #     logradouro_sacador_avalista=self.logradouro_sacador_avalista,
            #     bairro_sacador_avalista=self.bairro_sacador_avalista,
            #     cidade_sacador_avalista=self.cidade_sacador_avalista,
            #     uf_sacador_avalista=self.uf_sacador_avalista,
            #     cep_sacador_avalista=self.cep_sacador_avalista,
            # ),

            tipo_carteira_titulo=self.carteira,

            moeda=dict(
                codigo_moeda_cnab=self.codigo_moeda_cnab,
            ),

            titulo_aceite=self.titulo_aceite,
            nosso_numero=self.nosso_numero,
            digito_verificador_nosso_numero=str(self.dv_nosso_numero),
            data_vencimento=str(self.data_vencimento),
            valor_cobrado=self.valor_documento.replace('.', '').zfill(17),
            especie=self.especie,
            data_emissao=str(self.data_documento),
            tipo_pagamento=self.tipo_pagamento,
            indicador_pagamento_parcial=self.indicador_pagamento_parcial,

            juros=dict(
                tipo_juros=self.tipo_juros,
            ),

            multa=dict(
                tipo_multa=self.tipo_multa,
            ),

            grupo_desconto=dict(
                tipo_desconto=self.tipo_desconto,
            ),

            recebimento_divergente=dict(
                tipo_autorizacao_recebimento=self.tipo_autorizacao_recebimento,
            ),
        )

        return data
