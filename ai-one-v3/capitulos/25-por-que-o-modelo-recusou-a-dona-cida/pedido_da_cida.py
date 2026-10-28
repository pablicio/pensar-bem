"""O pedido de março da Dona Cida, pronto para o modelo."""
from risco.alvo import carteira
from risco.dados import com_variaveis
from risco.finalidade import com_divida


def pedido_da_cida():
    e = carteira()
    pedido = e[e["cliente_id"] == "C00000"].tail(1)
    return com_divida(com_variaveis(pedido))
