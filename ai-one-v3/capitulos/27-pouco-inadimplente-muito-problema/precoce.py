"""O alvo raro: parar de pagar logo nas primeiras parcelas."""
from risco.dados import lacrar, tabela, treino_validacao


def com_precoce(t):
    t = t.copy()
    dias = (t["data_atraso_90"] - t["data_concessao"]).dt.days
    # parou na 1ª ou 2ª parcela: 90 dias depois, até 150 dias
    t["precoce"] = (dias <= 150).astype(int)
    return t


def divisao():
    aberto, _ = lacrar(com_precoce(tabela()))
    return treino_validacao(aberto)
