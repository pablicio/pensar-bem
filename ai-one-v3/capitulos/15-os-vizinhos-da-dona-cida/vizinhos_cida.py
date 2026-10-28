import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from risco.dados import com_variaveis, tabela, treino_validacao
from risco.modelos import NUMERICAS

treino, _ = treino_validacao(tabela())
e = pd.read_csv("dados/brutos/emprestimos.csv")
cida = com_variaveis(e[e["cliente_id"] == "C00000"].tail(1))

escala = StandardScaler().fit(treino[NUMERICAS])
A = escala.transform(treino[NUMERICAS])
c = escala.transform(cida[NUMERICAS])

# à mão: a distância euclidiana do volume 1 a cada empréstimo
d = np.sqrt(((A - c) ** 2).sum(axis=1))
perto = np.argsort(d)[:5]
clientes = pd.read_csv("dados/brutos/clientes.csv")
nomes = clientes.set_index("cliente_id")["nome"]
for i in perto:
    v = treino.iloc[i]
    fim = "pagou" if v["alvo"] == 0 else "90 dias"
    print(f"{nomes[v['cliente_id']]:16} {v['tipo_negocio']:20}"
          f" {d[i]:5.2f}  {fim}")
p_mao = treino["alvo"].iloc[perto].mean()
print(f"probabilidade à mão:  {p_mao:.2f}")

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(A, treino["alvo"])
p_knn = knn.predict_proba(c)[0, 1]
print(f"KNeighborsClassifier: {p_knn:.2f}")
