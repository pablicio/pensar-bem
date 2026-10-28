import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import ParameterSampler

from botoes import BOTOES, COL
from risco.dados import lacrar, tabela, treino_validacao
from risco.finalidade import com_divida
from risco.modelos import boosting

aberto, teste = lacrar(com_divida(tabela()))
treino, valid = treino_validacao(aberto)
alvo = valid["alvo"].to_numpy()

# cem combinações de botões; guarda as notas na validação
notas = []
for botoes in ParameterSampler(BOTOES, 100, random_state=1):
    modelo = boosting().set_params(**botoes)
    modelo.fit(treino[COL], treino["alvo"])
    notas.append(modelo.predict_proba(valid[COL])[:, 1])
inteira = [roc_auc_score(alvo, n) for n in notas]

# o jeito do Ícaro: escolher olhando 500 empréstimos
sorteio = np.random.default_rng(0)
print("amostra  campeão nos 500  o mesmo na validação")
for i in range(1, 9):
    s = sorteio.choice(len(alvo), size=500, replace=False)
    nos_500 = [roc_auc_score(alvo[s], n[s]) for n in notas]
    c = int(np.argmax(nos_500))
    print(f"{i:7} {nos_500[c]:16.3f} {inteira[c]:21.3f}")
print(f"\no melhor dos cem na validação: {max(inteira):.3f}")
