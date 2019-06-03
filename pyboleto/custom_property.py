# -*- coding: utf-8 -*-


class CustomProperty(object):
    """Função para criar propriedades nos boletos

    Cria propriedades com getter, setter e delattr.

    Propriedades criadas com essa função sempre são strings internamente.

    O Setter sempre tentará remover qualquer digito verificador se existir.

    Aceita um numero com ou sem DV e remove o DV caso exista. Então preenxe
    com zfill até o tamanho adequado. Note que sempre que possível não use DVs
    ao entrar valores no pyboleto. De preferência o pyboleto vai calcular
    todos os DVs quando necessário.

    :param name: O nome da propriedade.
    :type name: string
    :param length: Tamanho para preencher com '0' na frente.
    :type length: integer

    """
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self._instance_state = {}

    def __set__(self, instance, value):
        if instance is None:
            raise TypeError("can't modify custom class properties")
        if '-' in value:
            values = value.split('-')
            values[0] = values[0].zfill(self.length)
            value = '-'.join(values)
        else:
            value = value.zfill(self.length)
        self._instance_state[instance] = value

    def __get__(self, instance, class_):
        if instance is None:
            return self
        return self._instance_state.get(instance, '0' * self.length)
