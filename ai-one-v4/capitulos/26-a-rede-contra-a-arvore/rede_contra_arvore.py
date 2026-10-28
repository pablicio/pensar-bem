import pandas as pd
import torch
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import log_loss, roc_auc_score
from torch import nn
from torch.utils.data import TensorDataset

from leitora.treino import fixar_semente, lotes, treinar_epoca

t = pd.read_csv("dados/abstencao.csv")
t["cidade"] = t["cidade"].astype("category")
t["inverno"] = t["edicao"].str.startswith("inverno")
teste = (t["edicao"] == "inverno 2026").to_numpy(copy=True)
X, y = t.drop(columns=["edicao", "faltou"]), t["faltou"]


def avalia(nome, p):
    """Por candidato e por cidade, no inverno de 2026."""
    alvo = y[teste]
    soma = pd.DataFrame({"cidade": t["cidade"][teste],
                         "previsto": p, "faltou": alvo})
    c = soma.groupby("cidade", observed=True).sum()
    erro = (c["previsto"] - c["faltou"]).abs().sum()
    print(f"{nome:24} {log_loss(alvo, p):8.4f}"
          f" {roc_auc_score(alvo, p):6.3f} {erro:7.0f}")


def rede(A, semente):
    """Treina o MLP e devolve a probabilidade no teste."""
    fixar_semente(semente)
    mlp = nn.Sequential(nn.Linear(A.shape[1], 64), nn.ReLU(),
                        nn.Linear(64, 64), nn.ReLU(),
                        nn.Linear(64, 1), nn.Flatten(0))
    otimizador = torch.optim.Adam(mlp.parameters())
    alvo = torch.tensor(y.to_numpy(), dtype=torch.float32)
    treino = TensorDataset(A[~teste], alvo[~teste])
    carregador = lotes(treino, 256, semente=semente)
    for epoca in range(10):
        treinar_epoca(mlp, carregador, otimizador,
                      nn.BCEWithLogitsLoss())
    with torch.no_grad():
        return torch.sigmoid(mlp.eval()(A[teste])).numpy()


print(f"{'':24} {'log loss':>8} {'AUC':>6} {'cidade':>7}")
anterior = t[t["edicao"] == "inverno 2025"]
taxa = anterior.groupby("cidade", observed=True)["faltou"]
avalia("taxa do inverno anterior",
       t["cidade"][teste].map(taxa.mean()).astype(float))

for semente in range(3):
    arvore = HistGradientBoostingClassifier(
        categorical_features="from_dtype",
        random_state=semente)
    arvore.fit(X[~teste], y[~teste])
    p = arvore.predict_proba(X[teste])[:, 1]
    avalia(f"árvores, semente {semente}", p)

colunas = pd.get_dummies(X, columns=["cidade"]).astype(float)
crua = torch.tensor(colunas.to_numpy(), dtype=torch.float32)
media, desvio = crua[~teste].mean(0), crua[~teste].std(0)
avalia("MLP crua, semente 0", rede(crua, 0))
for semente in range(3):
    avalia(f"MLP, semente {semente}",
           rede((crua - media) / desvio, semente))
