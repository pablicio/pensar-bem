"""Os pedidos de 2027, ainda sem história de pagamento."""
from risco.alvo import carteira
from risco.dados import com_variaveis

COLUNAS = ["valor", "parcelas", "faturamento_declarado",
           "comprometimento", "idade", "tempo_negocio_meses",
           "cliente_desde_meses", "emprestimos_anteriores",
           "online"]


def recentes():
    t = com_variaveis(carteira())
    # quantos clientes diferentes deram o mesmo telefone
    por_fone = t.groupby("telefone_referencia")["cliente_id"]
    t["mesmo_telefone"] = t["telefone_referencia"].map(
        por_fone.nunique())
    t["online"] = (t["canal"] == "online").astype(int)
    return t[t["data_concessao"] >= "2027-01-01"].copy()
