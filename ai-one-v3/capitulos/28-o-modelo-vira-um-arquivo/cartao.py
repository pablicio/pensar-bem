import hashlib
import textwrap
from pathlib import Path

import skops.io as sio
from sklearn.metrics import roc_auc_score

from risco.campeao import BOTOES, COLUNAS_FINAIS, campeao
from risco.dados import lacrar, tabela, treino_validacao
from risco.finalidade import com_divida

VERSAO = "1.0.0"
arquivo = Path("modelos") / f"campeao-{VERSAO}.skops"
confiaveis = sio.get_untrusted_types(file=arquivo)
modelo = sio.load(arquivo, trusted=confiaveis)
aberto, teste = lacrar(com_divida(tabela()))
treino, valid = treino_validacao(aberto)
X = COLUNAS_FINAIS


def auc(m, t):
    nota = m.predict_proba(t[X])[:, 1]
    return roc_auc_score(t["alvo"], nota)


# a validação mede o mesmo modelo treinado só no passado
so_treino = campeao().fit(treino[X], treino["alvo"])
notas = modelo.predict_proba(teste[X])[:, 1].round(6)
digital = hashlib.sha256(notas.tobytes()).hexdigest()[:16]
inicio = aberto["data_concessao"].min().date()
fim = aberto["data_concessao"].max().date()
botoes = ", ".join(f"{k}={v}" for k, v in BOTOES.items())
botoes = textwrap.fill(f"Botões: {botoes}.", 63)
colunas = textwrap.fill(f"Colunas: {', '.join(X)}.", 63)

cartao = f"""# Cartão do modelo: campeão {VERSAO}

Uso: ordenar pedidos de crédito pelo risco de chegar a
90 dias de atraso em 12 meses. Não decide sozinho: recusas por
pouco têm segunda leitura (decisão de 4/5/2027). Não detecta
fraude (fila de anomalias à parte).

Dados: {len(aberto):,} empréstimos concedidos de {inicio} a
{fim}; {aberto['alvo'].mean():.1%} chegaram a 90 dias.
Modelo: boosting de árvores de um nível.
{botoes}
{colunas}

AUC na validação (jul–nov/2025):  {auc(so_treino, valid):.3f}
AUC no teste (dez/2025–mar/2026): {auc(modelo, teste):.3f}

Limites conhecidos: usa o faturamento declarado (quem declara
menos parece mais arriscado); aprova de 55% a 67% conforme a
região; não sabe nada do que mudou depois de novembro de 2025.
Digital das notas no teste: {digital}
"""
(Path("modelos") / f"cartao-{VERSAO}.md").write_text(
    cartao, encoding="utf-8")
print(cartao)
