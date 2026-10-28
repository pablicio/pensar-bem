import numpy as np
from sklearn.tree import DecisionTreeClassifier

from risco.alvo import carteira
from risco.dados import com_variaveis, tabela, treino_validacao
from risco.modelos import NUMERICAS

treino, _ = treino_validacao(tabela())
e = carteira()
cida = com_variaveis(e[e["cliente_id"] == "C00000"].tail(1))

sorteio = np.random.default_rng(0)
for i in range(8):
    # uma amostra do treino do mesmo tamanho, com reposição
    linhas = sorteio.choice(len(treino), size=len(treino))
    amostra = treino.iloc[linhas]
    arvore = DecisionTreeClassifier(min_samples_leaf=200,
                                    random_state=0)
    arvore.fit(amostra[NUMERICAS], amostra["alvo"])
    risco = arvore.predict_proba(cida[NUMERICAS])[0, 1]
    print(f"árvore {i + 1}: {risco:5.1%}")
