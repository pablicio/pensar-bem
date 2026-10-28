"""Quatro vestibulares passados: quem faltou à prova."""
from pathlib import Path

import numpy as np
import pandas as pd

CIDADES = ["Guarapuava", "Pitanga", "Laranjeiras do Sul",
           "Prudentópolis", "Palmital", "Turvo", "Candói",
           "Irati"]
FRACAO = [0.40, 0.10, 0.10, 0.10, 0.07, 0.08, 0.07, 0.08]
PESO_CIDADE = [0.0, 0.3, 0.1, -0.2, 0.5, 0.4, 0.2, -0.1]
EDICOES = {"verão 2025": 24_000, "inverno 2025": 22_000,
           "verão 2026": 24_000, "inverno 2026": 22_000}

sorteio = np.random.default_rng(27)
partes = []
for edicao, n in EDICOES.items():
    c = sorteio.choice(len(CIDADES), n, p=FRACAO)
    df = pd.DataFrame({
        "edicao": edicao,
        "cidade": np.array(CIDADES)[c],
        "idade": (16 + sorteio.gamma(2.0, 2.5, n)).round(),
        "distancia_km": sorteio.lognormal(1.8, 1, n).round(1),
        "treineiro": sorteio.random(n) < 0.15,
        "isento": sorteio.random(n) < 0.3,
        "dias_antes_do_prazo": sorteio.integers(0, 60, n),
        "concorrencia": sorteio.lognormal(1.8, .7, n).round(1),
    })
    inverno = edicao.startswith("inverno")
    z = (-2.3 + np.array(PESO_CIDADE)[c]
         + 1.6 * (df["distancia_km"] > 40)
         + 0.9 * df["isento"]
         + 1.3 * (df["treineiro"] & inverno)
         + 0.8 * (df["dias_antes_do_prazo"] < 3)
         - 0.5 * (df["concorrencia"] > 15)
         + 0.7 * (df["idade"] > 30))
    df["faltou"] = sorteio.random(n) < 1 / (1 + np.exp(-z))
    partes.append(df)

tabela = pd.concat(partes, ignore_index=True)
Path("dados").mkdir(exist_ok=True)
tabela.to_csv("dados/abstencao.csv", index=False)
resumo = tabela.groupby("edicao", sort=False)["faltou"]
print(resumo.agg(["size", "mean"]).round(3))
