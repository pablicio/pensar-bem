"""O mundo da Coopersol: datas, usinas, tarifa e o sorteio."""
from datetime import date, timedelta
from pathlib import Path

import numpy as np

BRUTOS = Path("dados/brutos")
INICIO = date(2026, 3, 1)
DIAS = 396                  # de 1/3/2026 a 31/3/2027
PASSOS = 288                # leituras de 5 minutos por dia
TARIFA = 0.9412             # R$ por kWh compensado
USINAS = {                  # fabricante, MW, inversores
    "corumba": ("A", 2.5, 64),
    "cocalzinho": ("B", 1.8, 46),
    "abadiania": ("C", 1.2, 30),
}
COOPERADOS = {"corumba": 882, "cocalzinho": 635,
              "abadiania": 423}
FIRMWARE = (date(2027, 2, 9), date(2027, 2, 11))  # kWh
API_V2 = date(2027, 2, 12)  # a API do B passa a usar UTC
RECADASTRO = 39             # CPFs que perdem o zero
rng = np.random.default_rng(2027)


def dia(d):
    return INICIO + timedelta(days=d)


def br(valor, casas):
    # 1234.5 -> "1.234,5"
    texto = f"{valor:,.{casas}f}"
    return texto.translate(str.maketrans(",.", ".,"))


def meses():
    d = 0
    while d < DIAS:
        hoje = dia(d)
        inicio = d
        while d < DIAS and dia(d).month == hoje.month:
            d += 1
        yield hoje.strftime("%Y-%m"), inicio, d


def gravar(arquivo, linhas, encoding):
    # uma linha por item, terminada em \n em qualquer sistema
    texto = "\n".join(linhas) + "\n"
    arquivo.write_text(texto, encoding=encoding, newline="\n")
