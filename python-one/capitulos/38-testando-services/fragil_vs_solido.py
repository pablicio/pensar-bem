# frágil: verifica como
def test_ruim(servico, repo):
    servico.criar("Tomate", Decimal("8.90"), 1)
    repo.buscar_por_nome.assert_called_once_with("Tomate")


# sólido: verifica o quê
def test_bom(servico):
    servico.criar("Tomate", Decimal("8.90"), 1)
    with pytest.raises(ProdutoJaExiste):
        servico.criar("Tomate", Decimal("9.10"), 1)
