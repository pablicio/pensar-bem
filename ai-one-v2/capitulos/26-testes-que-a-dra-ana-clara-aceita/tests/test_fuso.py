import pandas as pd

from rateio.fuso import cocalzinho_local


def test_cocalzinho_meio_dia():
    # causa 3: meio-dia em Goiás, escrito nos dois formatos
    inicio = pd.Series(["2027-02-11T12:00:00",
                        "2027-02-15T15:00:00Z"])
    local = cocalzinho_local(inicio)
    assert local.dt.hour.tolist() == [12, 12]
