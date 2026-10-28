import pandas as pd

from rateio.limpeza import corumba_em_kwh, cpf_normalizado


def test_cpf_com_e_sem_ponto():
    # causa 1: o CPF que perdeu o zero
    cpfs = pd.Series(["060.419.765-98", "6041976598"])
    certos = ["06041976598", "06041976598"]
    assert cpf_normalizado(cpfs).tolist() == certos


def test_corumba_em_kwh():
    # causa 2: dia em Wh (8/2) e dia em kWh (10/2)
    a = pd.DataFrame({"Data": ["08/02/2027", "08/02/2027",
                               "10/02/2027", "10/02/2027"],
                      "Energia": [1234.5, 0.0, 1.2345, 0.0]})
    assert corumba_em_kwh(a).tolist() == [1.2345, 0, 1.2345, 0]
