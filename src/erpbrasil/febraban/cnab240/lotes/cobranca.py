
from erpbrasil.febraban.cnab240.tipos import Lote


class LoteCobranca(Lote):
    HeaderCls = LoteCobranca.banco.registros.HeaderLoteCobranca
    TrailerCls = LoteCobranca.banco.registros.TrailerLoteCobranca
