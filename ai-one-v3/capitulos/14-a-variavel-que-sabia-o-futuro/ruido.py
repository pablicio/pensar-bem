import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (StratifiedKFold,
                                     cross_val_score)
from sklearn.pipeline import make_pipeline

from risco.dados import tabela, treino_validacao

treino, _ = treino_validacao(tabela())
y = treino["alvo"].to_numpy()
sorteio = np.random.default_rng(0)
ruido = sorteio.normal(size=(len(y), 2000))  # puro acaso
dobras = StratifiedKFold(5, shuffle=True, random_state=0)

# errado: escolhe as 20 "melhores" olhando a tabela inteira
seletor = SelectKBest(f_classif, k=20)
escolhidas = seletor.fit_transform(ruido, y)
errado = cross_val_score(LogisticRegression(), escolhidas, y,
                         cv=dobras, scoring="roc_auc")
# certo: a escolha faz parte do modelo, dentro de cada dobra
modelo = make_pipeline(SelectKBest(f_classif, k=20),
                       LogisticRegression())
certo = cross_val_score(modelo, ruido, y, cv=dobras,
                        scoring="roc_auc")
print(f"escolhendo antes de dividir: AUC {errado.mean():.3f}")
print(f"escolhendo dentro da dobra:  AUC {certo.mean():.3f}")
