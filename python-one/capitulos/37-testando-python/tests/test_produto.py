def test_repor_aumenta_o_estoque(produto):
    produto.repor(20)
    assert produto.estoque == 120
