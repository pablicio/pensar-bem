import numpy as np

from rateio.calculo import credito, sobra


def test_credito_do_seu_dirceu():
    assert credito(126809.824, 1.3954) == (1769.5, 1665.45)


def test_sobra_e_so_arredondamento():
    # vale para qualquer geração: no máximo um centavo
    # por cooperado
    cotas = [33.3333, 33.3333, 33.3334]
    rng = np.random.default_rng(2027)
    for geracao in rng.uniform(10_000, 300_000, size=1000):
        reais = [credito(geracao, c)[1] for c in cotas]
        assert abs(sobra(geracao, reais)) <= 0.01 * len(cotas)
