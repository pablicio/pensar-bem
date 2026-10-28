"""As fontes brutas, cada uma no seu formato."""
import json
from pathlib import Path

import pandas as pd

BRUTOS = Path("dados/brutos")


def ler_corumba(mes):
    """Fabricante A: Latin-1, ';', valores em Wh."""
    pasta = BRUTOS / "inversores/corumba"
    caminho = pasta / f"corumba_{mes}.csv"
    return pd.read_csv(caminho, sep=";", skiprows=1,
                       encoding="latin-1", decimal=",",
                       thousands=".")


def ler_cocalzinho(dias):
    """Fabricante B: um JSON da API por dia."""
    pasta = BRUTOS / "inversores/cocalzinho"
    partes = []
    for dia in dias:
        caminho = pasta / f"{dia}.json"
        corpo = json.loads(caminho.read_text(encoding="utf-8"))
        partes.append(pd.DataFrame(corpo["leituras"]))
    return pd.concat(partes, ignore_index=True)


def ler_abadiania(mes):
    """Fabricante C: UTF-8 com BOM, kWh."""
    pasta = BRUTOS / "inversores/abadiania"
    return pd.read_csv(pasta / f"abadiania_{mes}.csv",
                       encoding="utf-8-sig")


def ler_cadastro():
    return pd.read_excel(BRUTOS / "cadastro_cooperados.xlsx",
                         dtype={"CPF": "string"})


def ler_envio(mes):
    return pd.read_csv(BRUTOS / "envios" / f"rateio_{mes}.csv",
                       sep=";", decimal=",", thousands=".",
                       dtype={"CPF": "string"})
