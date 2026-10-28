"""O modelo do arquivo e os pedidos que ele recebeu."""
import pandas as pd
import skops.io as sio

from risco.campeao import COLUNAS_FINAIS
from risco.dados import com_variaveis, lacrar, tabela
from risco.finalidade import com_divida

ARQUIVO = "modelos/campeao-1.0.0.skops"


def modelo():
    tipos = sio.get_untrusted_types(file=ARQUIVO)
    return sio.load(ARQUIVO, trusted=tipos)


def referencia():
    """O que o modelo viu no treino: tudo fora do lacre."""
    aberto, _ = lacrar(com_divida(tabela()))
    return aberto


def pedidos():
    """Os pedidos de 15/3 a 11/6, com a cobrança de 14/6."""
    p = pd.read_csv("dados/brutos/producao_pedidos.csv",
                    parse_dates=["data_concessao"])
    cob = pd.read_csv("dados/brutos/producao_cobranca.csv")
    p = com_divida(com_variaveis(p))
    return p.merge(cob, on="pedido_id")


def notas(m, t):
    return m.predict_proba(t[COLUNAS_FINAIS])[:, 1]
