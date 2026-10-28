from rateio.calculo import credito


def test_cota_zero_nao_recebe_nada():
    assert credito(126809.824, 0) == (0.0, 0.0)
