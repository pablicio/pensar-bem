"""Regressão: a reconciliação de fevereiro, no centavo."""
import pytest

from rateio.calculo import TARIFA
from rateio.reconciliacao import reconcilia


@pytest.fixture(scope="module")
def fevereiro():
    return reconcilia("2027-02")


def test_credito_que_faltou(fevereiro):
    assert round(fevereiro["faltou"].sum(), 2) == 47_312.18


def test_os_vinte_centavos(fevereiro):
    faltou = fevereiro["faltou"].sum()
    um_a_um = faltou - fevereiro["faltou_kwh"] * TARIFA
    sobra = fevereiro["sobra_kwh"] * TARIFA
    diferenca = faltou - fevereiro["sede_reais"]
    esperado = pytest.approx(um_a_um - sobra, abs=0.005)
    assert diferenca == esperado
