import pandas as pd
import pytest

from rateio.leitura import BRUTOS
from rateio.reconciliacao import SEDE

MESES = [str(m) for m in pd.period_range("2026-03", "2027-02",
                                         freq="M")]


@pytest.mark.parametrize("mes", MESES)
def test_sede_so_recebe_arredondamento(mes):
    arquivo = BRUTOS / f"ged/compensacao/compensacao_{mes}.csv"
    ged = pd.read_csv(arquivo, sep=";", encoding="latin-1",
                      decimal=",", thousands=".")
    valor = ged.loc[ged["Nome"] == SEDE, "Valor (R$)"].iloc[0]
    assert abs(valor) <= 1.00
