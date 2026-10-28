import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.pipeline import Pipeline

from risco.dados import tabela, treino_validacao
from risco.modelos import COLUNAS, logistica, preparacao

FAIXAS = [0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 1]


def balanceada():
    """A logística com classes 'balanceadas', como em SP."""
    pesos = LogisticRegression(max_iter=5_000,
                               class_weight="balanced")
    return Pipeline([("prepara", preparacao()),
                     ("modelo", pesos)])


def por_faixa(p, y):
    faixa = pd.cut(p, FAIXAS)
    tabela = pd.DataFrame({"previsto": p, "real": y})
    grupos = tabela.groupby(faixa, observed=True)
    return grupos.agg(previsto=("previsto", "mean"),
                      real=("real", "mean"),
                      n=("real", "size"))


if __name__ == "__main__":
    treino, valid = treino_validacao(tabela())
    y = valid["alvo"].to_numpy()
    for nome, modelo in [("logística", logistica()),
                         ("balanceada", balanceada())]:
        modelo.fit(treino[COLUNAS], treino["alvo"])
        p = modelo.predict_proba(valid[COLUNAS])[:, 1]
        print(f"{nome}: AUC {roc_auc_score(y, p):.3f},"
              f" Brier {brier_score_loss(y, p):.4f},"
              f" média prevista {p.mean():.1%}")
        print(por_faixa(p, y).round(3).to_string())
        print()
