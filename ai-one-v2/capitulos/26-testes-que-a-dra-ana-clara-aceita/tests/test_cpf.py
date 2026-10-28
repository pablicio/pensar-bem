import pytest

from rateio.cpf import CPFInvalido, confere_cpf, normaliza_cpf


@pytest.mark.parametrize("escrito", ["060.419.765-98",
                                     "6041976598"])
def test_normaliza_qualquer_escrita(escrito):
    assert normaliza_cpf(escrito) == "06041976598"


def test_confere_cpf_valido():
    assert confere_cpf("060.419.765-98") == "06041976598"


@pytest.mark.parametrize("errado", ["060.419.765-99",
                                    "060.419.765-9O", "123"])
def test_confere_cpf_recusa(errado):
    with pytest.raises(CPFInvalido):
        confere_cpf(errado)
