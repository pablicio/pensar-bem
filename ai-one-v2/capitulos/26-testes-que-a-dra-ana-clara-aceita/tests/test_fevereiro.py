"""Regressão: o erro de fevereiro de 2027 não pode voltar."""
import pytest

from rateio.calculo import credito
from rateio.geracao import geracao_diaria
from rateio.leitura import ler_cadastro

FEVEREIRO = {"Abadiânia": 126809.824,
             "Cocalzinho": 186790.392,
             "Corumbá de Goiás": 259313.777}


@pytest.fixture(scope="module")
def geracao():
    leituras = geracao_diaria("2027-02")
    return leituras.groupby("usina")["kwh"].sum().round(3)


def test_geracao_por_usina(geracao):
    esperado = pytest.approx(FEVEREIRO, abs=0.01)
    assert geracao.to_dict() == esperado


def test_credito_total(geracao):
    cad = ler_cadastro()
    ativos = cad[cad["Situação"] == "Ativo"]
    pares = zip(ativos["Usina"], ativos["Cota (%)"])
    reais = [credito(geracao[u], c)[1] for u, c in pares]
    assert round(sum(reais), 2) == 539_226.73
