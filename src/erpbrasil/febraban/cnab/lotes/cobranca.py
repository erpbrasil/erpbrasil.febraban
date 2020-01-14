
from erpbrasil.febraban.cnab.tipos import Lote


class LoteCobranca(Lote):
    HeaderCls = LoteCobranca.banco.registros.HeaderLoteCobranca
    TrailerCls = LoteCobranca.banco.registros.TrailerLoteCobranca
