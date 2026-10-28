from pedido_da_cida import pedido_da_cida
from risco.campeao import COLUNAS_FINAIS, treinado
from risco.dados import lacrar, tabela
from risco.explica import e_se
from risco.finalidade import com_divida


def mostra(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return str(v)
    return f"{v:,.2f}".rstrip("0").rstrip(".")


modelo = treinado()
aberto, _ = lacrar(com_divida(tabela()))
risco, efeitos = e_se(modelo, pedido_da_cida(), aberto,
                      COLUNAS_FINAIS)
print(f"Dona Cida, o campeão: {risco:.1%}\n")
efeitos["muda"] = 100 * efeitos["muda"]
print(efeitos.map(mostra).to_string())
