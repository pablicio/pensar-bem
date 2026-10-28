"""As políticas que o banco compara, no teste fora do tempo."""
import numpy as np

from em_producao import modelo, notas
from regra_jussara import regras_da_jussara
from risco.campeao import COLUNAS_FINAIS, campeao
from risco.dados import lacrar, tabela, treino_validacao
from risco.finalidade import com_divida
from risco.lucro import ganho


def corte_da_validacao():
    """O corte de maior lucro, escolhido sem olhar o teste."""
    aberto, _ = lacrar(com_divida(tabela()))
    treino, valid = treino_validacao(aberto)
    m = campeao().fit(treino[COLUNAS_FINAIS], treino["alvo"])
    nota = m.predict_proba(valid[COLUNAS_FINAIS])[:, 1]
    valores = ganho(valid)
    cortes = np.arange(0.04, 0.40, 0.01).round(2)
    lucros = [valores[nota < c].sum() for c in cortes]
    return float(cortes[int(np.argmax(lucros))])


def politicas():
    """O teste, os ganhos e quem cada política aprova."""
    _, teste = lacrar(com_divida(tabela()))
    nota = notas(modelo(), teste)
    jussara = regras_da_jussara(teste).all(axis=1).to_numpy()
    posicao = nota.argsort().argsort()
    mesma = posicao < jussara.mean() * len(nota)
    corte = corte_da_validacao()
    return teste, ganho(teste), {
        "regra da Jussara": jussara,
        "modelo, mesma aprovação": mesma,
        f"modelo, corte de {corte:.2f}": nota < corte,
        "aprovar todos": np.ones(len(nota), dtype=bool)}
