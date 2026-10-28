import json
from pathlib import Path

import pandas as pd

brutos = Path("dados/brutos/inversores")


def ler_a(mes):
    """Fabricante A: Latin-1, ';', uma linha de título."""
    caminho = brutos / "corumba" / f"corumba_{mes}.csv"
    return pd.read_csv(caminho, sep=";", skiprows=1,
                       encoding="latin-1", decimal=",",
                       thousands=".")


def ler_b(dias):
    """Fabricante B: um JSON da API por dia."""
    partes = []
    for dia in dias:
        caminho = brutos / "cocalzinho" / f"{dia}.json"
        corpo = json.loads(caminho.read_text(encoding="utf-8"))
        partes.append(pd.DataFrame(corpo["leituras"]))
    return pd.concat(partes, ignore_index=True)


def ler_c(mes):
    """Fabricante C: UTF-8 com BOM, vírgula entre campos."""
    pasta = brutos / "abadiania"
    return pd.read_csv(pasta / f"abadiania_{mes}.csv",
                       encoding="utf-8-sig")


a = ler_a("2027-02")
b = ler_b(pd.date_range("2027-02-01", "2027-02-28").date)
c = ler_c("2027-02")
for nome, tabela in [("A", a), ("B", b), ("C", c)]:
    tipos = [str(t) for t in tabela.dtypes]
    print(nome, tabela.shape, tipos)

print("geração de fevereiro, em kWh:")
print(f"  Corumbá    {a['Energia'].sum() / 1000:11,.2f}")
positivos = b["energia_kwh"].clip(lower=0)
print(f"  Cocalzinho {positivos.sum():11,.2f}")
print(f"  Abadiânia  {c['energy_kwh'].sum():11,.2f}")
