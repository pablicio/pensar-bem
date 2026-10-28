import pytest


def test_nao_vende_mais_do_que_tem():
    produto = Produto(nome="Tomate", preco=Decimal("8.90"),
                      estoque=10)

    with pytest.raises(EstoqueInsuficiente) as erro:
        produto.vender(30)

    assert erro.value.disponivel == 10
    assert erro.value.pedido == 30
    assert produto.estoque == 10
