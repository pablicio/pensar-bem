"""A geração diária de cada inversor, já corrigida."""
import pandas as pd

from rateio.leitura import (ler_abadiania, ler_cocalzinho,
                            ler_corumba)
from rateio.limpeza import corumba_em_kwh


def dias_do_mes(mes):
    """Os dias de um mês 'AAAA-MM', como 'AAAA-MM-DD'."""
    inicio = pd.Timestamp(f"{mes}-01")
    fim = inicio + pd.offsets.MonthEnd(0)
    return [str(d.date()) for d in pd.date_range(inicio, fim)]


def geracao_diaria(mes):
    """kWh por inversor e por dia, nas três usinas, num mês."""
    a = ler_corumba(mes)
    data_a = (a["Data"].str[6:] + "-" + a["Data"].str[3:5]
              + "-" + a["Data"].str[:2])
    partes = [pd.DataFrame({"usina": "Corumbá de Goiás",
                            "inversor": a["Inversor"],
                            "data": data_a,
                            "kwh": corumba_em_kwh(a)})]
    for dia in dias_do_mes(mes):
        b = ler_cocalzinho([dia])
        kwh_b = b["energia_kwh"].clip(lower=0)
        partes.append(pd.DataFrame({
            "usina": "Cocalzinho", "inversor": b["inversor"],
            "data": dia, "kwh": kwh_b}))
    c = ler_abadiania(mes)
    data_c = c["timestamp"].str[:10]
    partes.append(pd.DataFrame({"usina": "Abadiânia",
                                "inversor": c["inverter"],
                                "data": data_c,
                                "kwh": c["energy_kwh"]}))
    leituras = pd.concat(partes, ignore_index=True)
    chave = ["usina", "inversor", "data"]
    return leituras.groupby(chave, as_index=False)["kwh"].sum()
