"""Leitura das fontes brutas, cada uma no seu formato."""
import json
from pathlib import Path

import pandas as pd

FUSO = "America/Sao_Paulo"
USINAS = ["Corumbá de Goiás", "Cocalzinho", "Abadiânia"]


def ler_corumba(pasta: Path, mes: str) -> pd.DataFrame:
    """Fabricante A: Latin-1, ';', vírgula decimal, Wh (ou kWh)."""
    df = pd.read_csv(pasta / "inversores" / "corumba"
                     / f"corumba_{mes}.csv",
                     sep=";", skiprows=1, encoding="latin-1",
                     decimal=",", thousands=".")
    df["inicio"] = pd.to_datetime(df["Data"] + " " + df["Hora"],
                                  format="%d/%m/%Y %H:%M")
    df["inicio"] = df["inicio"].dt.tz_localize(FUSO)
    return pd.DataFrame({"usina": USINAS[0],
                         "inversor": df["Inversor"],
                         "inicio": df["inicio"],
                         "valor": df["Energia"]})


def ler_cocalzinho(pasta: Path, mes: str) -> pd.DataFrame:
    """Fabricante B: um JSON por dia; horário local ou UTC."""
    inicio = pd.Timestamp(f"{mes}-01")
    dias = pd.date_range(inicio - pd.Timedelta(days=1),
                         inicio + pd.offsets.MonthEnd(0)
                         + pd.Timedelta(days=1))
    partes = []
    for d in dias:
        arquivo = (pasta / "inversores" / "cocalzinho"
                   / f"{d.date()}.json")
        if arquivo.exists():
            corpo = json.loads(arquivo.read_text(encoding="utf-8"))
            partes.append(pd.DataFrame(corpo["leituras"]))
    df = pd.concat(partes, ignore_index=True)
    utc = df["inicio"].str.endswith("Z")
    t = pd.to_datetime(df["inicio"].str.removesuffix("Z"))
    local = t.where(~utc, t - pd.Timedelta(hours=3))
    return pd.DataFrame({"usina": USINAS[1],
                         "inversor": df["inversor"],
                         "inicio": local.dt.tz_localize(FUSO),
                         "valor": df["energia_kwh"]})


def ler_abadiania(pasta: Path, mes: str) -> pd.DataFrame:
    """Fabricante C: UTF-8 com BOM, kWh com ponto."""
    df = pd.read_csv(pasta / "inversores" / "abadiania"
                     / f"abadiania_{mes}.csv",
                     encoding="utf-8-sig", parse_dates=["timestamp"])
    return pd.DataFrame({"usina": USINAS[2],
                         "inversor": df["inverter"],
                         "inicio": df["timestamp"].dt.tz_localize(FUSO),
                         "valor": df["energy_kwh"]})


def ler_cadastro(pasta: Path) -> pd.DataFrame:
    return pd.read_excel(pasta / "cadastro_cooperados.xlsx",
                         dtype={"CPF": "string"})


def ler_compensacao(pasta: Path, mes: str) -> pd.DataFrame:
    return pd.read_csv(pasta / "ged" / "compensacao"
                       / f"compensacao_{mes}.csv",
                       sep=";", encoding="latin-1", decimal=",",
                       thousands=".", dtype={"CPF": "string"})
