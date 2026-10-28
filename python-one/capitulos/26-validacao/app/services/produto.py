def criar(self, dados: ProdutoCriar) -> Produto:
    if self.repo.buscar_por_nome(dados.nome):
        raise ProdutoJaExiste(dados.nome)

    produtor = self.repo_produtor.buscar(dados.produtor_id)
    if produtor is None:
        raise ProdutorNaoEncontrado(dados.produtor_id)
    if not produtor.ativo:
        raise ProdutorInativo(produtor.id)

    if dados.preco < produtor.preco_minimo:
        raise PrecoAbaixoDoMinimo(produtor.preco_minimo)

    ...
