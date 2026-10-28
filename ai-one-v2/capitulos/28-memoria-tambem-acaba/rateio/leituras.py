"""Leituras de cinco minutos das três usinas, numa tabela."""
import pandas as pd

from rateio.fuso import FUSO, cocalzinho_local
from rateio.geracao import dias_do_mes
from rateio.leitura import (ler_abadiania, ler_cocalzinho,
                            ler_corumba)
from rateio.limpeza import corumba_em_kwh

USINAS = ["Corumbá de Goiás", "Cocalzinho", "Abadiânia"]


def leituras_do_mes(mes):
    """usina, inversor, instante em Brasília e kWh, com tipos
    que economizam memória."""
    a = ler_corumba(mes)
    instante_a = pd.to_datetime(a["Data"] + " " + a["Hora"],
                                format="%d/%m/%Y %H:%M")
    b = ler_cocalzinho(dias_do_mes(mes))
    c = ler_abadiania(mes)
    partes = [
        ("Corumbá de Goiás", a["Inversor"],
         instante_a.dt.tz_localize(FUSO), corumba_em_kwh(a)),
        ("Cocalzinho", b["inversor"],
         cocalzinho_local(b["inicio"]), b["energia_kwh"]),
        ("Abadiânia", c["inverter"],
         pd.to_datetime(c["timestamp"]).dt.tz_localize(FUSO),
         c["energy_kwh"]),
    ]
    tabela = pd.concat(
        [pd.DataFrame({"usina": u, "inversor": inv,
                       "instante": inst, "kwh": kwh})
         for u, inv, inst, kwh in partes], ignore_index=True)
    tipos = {"usina": pd.CategoricalDtype(USINAS),
             "inversor": "category"}
    return tabela.astype(tipos)
