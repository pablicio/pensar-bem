from rateio.geracao import geracao_diaria


def test_nenhum_dia_mil_vezes_menor():
    leituras = geracao_diaria("2027-02")
    por_dia = leituras.groupby(["usina", "data"])["kwh"].sum()
    media = por_dia.groupby("usina").transform("mean")
    assert (por_dia >= 0.2 * media).all()
