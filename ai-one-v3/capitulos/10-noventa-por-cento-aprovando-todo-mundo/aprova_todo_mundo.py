from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

from risco.dados import tabela, treino_validacao
from risco.modelos import COLUNAS, logistica

treino, valid = treino_validacao(tabela())
X, y = treino[COLUNAS], treino["alvo"]
Xv, yv = valid[COLUNAS], valid["alvo"]

todos = DummyClassifier(strategy="most_frequent")
modelos = {"aprova todo mundo": todos,
           "logística, corte de 0,5": logistica()}
for nome, modelo in modelos.items():
    modelo.fit(X, y)
    previsto = modelo.predict(Xv)
    matriz = confusion_matrix(yv, previsto)
    acuracia = accuracy_score(yv, previsto)
    print(f"{nome} (acurácia {acuracia:.1%})")
    print("                aprovado  recusado")
    for rotulo, linha in zip(["pagou", "não pagou"], matriz):
        print(f"  {rotulo:12} {linha[0]:9,} {linha[1]:9,}")
