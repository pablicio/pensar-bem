from rateio.leitura import ler_cadastro
from rateio.limpeza import cpf_normalizado


def test_todo_cpf_normalizado_tem_onze_algarismos():
    cpfs = cpf_normalizado(ler_cadastro()["CPF"])
    assert cpfs.str.fullmatch(r"\d{11}").all()
