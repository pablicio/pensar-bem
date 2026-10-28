from recentes import recentes
from risco.campeao import COLUNAS_FINAIS, treinado
from risco.dados import lacrar, tabela
from risco.explica import e_se
from risco.finalidade import com_divida

modelo = treinado()
aberto, _ = lacrar(com_divida(tabela()))
r = com_divida(recentes())
fone = r["telefone_referencia"]
conta = r[fone == "(71) 98877-1203"].head(1)
risco, efeitos = e_se(modelo, conta, aberto, COLUNAS_FINAIS)
print(f"uma das nove contas: {risco:.1%}")
print((100 * efeitos["muda"]).round(1).to_string())
