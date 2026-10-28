"""Gera as mensagens do canal da Defesa Civil, com semente."""
import csv
from pathlib import Path

import numpy as np
import pandas as pd

from dados.frases import (BAIRROS, CLASSES, RUAS, escreve_mal,
                          mensagem)

PASTA = Path("dados/brutos")
# as noites de chuva em que o canal já existia e quantas
# mensagens chegaram em cada uma
NOITES = [("2017-06-05 18:00", 1400),
          ("2019-01-20 19:00", 900),
          ("2020-07-08 17:00", 1100),
          ("2022-12-02 18:00", 1300),
          ("2023-10-07 16:00", 5200),
          ("2023-11-18 15:00", 6100),
          ("2024-06-21 18:00", 2600),
          ("2026-10-14 19:00", 1200)]
FORA = 9000                      # mensagens em dias comuns
# a mensagem da Dona Ivone, lida às três da manhã (capítulo 19)
IVONE = ("2026-10-14 23:42",
         "socorro to presa no segundo andar com minha neta "
         "de 6 anos o ribeirao encheu de repente, rua "
         "itoupava 412 vila nova, ivone",
         {"bairro": "Vila Nova", "rua": "rua Itoupava",
          "numero": 412, "pessoas": 2})
# a proporção de risco, ajuda, info e boato
PESO = {"risco": [.07, .17, .50, .26],
        "comum": [.01, .14, .80, .05]}


def sorteia_horas(sorteio, inicio, n):
    """n horários numa noite: muitos no começo."""
    minutos = sorteio.gamma(1.6, 140.0, size=n)
    return (pd.Timestamp(inicio)
            + pd.to_timedelta(minutos, "min"))


def uma(sorteio, classe):
    bairro = BAIRROS[int(sorteio.integers(len(BAIRROS)))]
    campos = {"bairro": bairro,
              "rua": RUAS[int(sorteio.integers(len(RUAS)))],
              "numero": int(sorteio.integers(1, 2400)),
              "pessoas": int(sorteio.choice(
                  [1, 2, 2, 3, 3, 4, 5, 6, 8, 12]))}
    texto, usados = mensagem(sorteio, classe, campos)
    return escreve_mal(sorteio, texto), usados


def main(semente=19):
    sorteio = np.random.default_rng(semente)
    linhas = []
    for inicio, n in NOITES:
        horas = sorteia_horas(sorteio, inicio, n)
        classes = sorteio.choice(CLASSES, size=n,
                                 p=PESO["risco"])
        linhas += list(zip(horas, classes))
    dias = pd.date_range("2016-01-01", "2027-02-28",
                         freq="min")
    horas = dias[np.sort(sorteio.integers(0, len(dias), FORA))]
    classes = sorteio.choice(CLASSES, size=FORA,
                             p=PESO["comum"])
    linhas += list(zip(horas, classes))
    linhas.append((pd.Timestamp(IVONE[0]), "ivone"))
    linhas.sort(key=lambda par: par[0])
    PASTA.mkdir(parents=True, exist_ok=True)
    with open(PASTA / "mensagens.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "data_hora", "texto", "verdade",
                    "classe", "bairro", "rua", "numero",
                    "pessoas"])
        for i, (hora, verdade) in enumerate(linhas, start=1):
            if verdade == "ivone":
                verdade, texto, c = "risco", IVONE[1], IVONE[2]
            else:
                texto, c = uma(sorteio, verdade)
            # a Júlia rotula às pressas: erra 3% das mensagens
            classe = verdade
            if sorteio.random() < 0.03:
                classe = str(sorteio.choice(CLASSES))
            w.writerow([i, hora.strftime("%Y-%m-%d %H:%M"),
                        texto, verdade, classe,
                        c.get("bairro", ""), c.get("rua", ""),
                        c.get("numero", ""),
                        c.get("pessoas", "")])
    print(len(linhas), "mensagens")


if __name__ == "__main__":
    main()
