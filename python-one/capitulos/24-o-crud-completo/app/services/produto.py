    def listar(
        self, limite: int = 20, pagina: int = 1
    ) -> list[Produto]:
        limite = max(1, min(limite, 100))
        pagina = max(1, pagina)
        return self.repo.listar(
            limite=limite, deslocamento=(pagina - 1) * limite
        )

    def atualizar(
        self, produto_id: int, dados: ProdutoCriar
    ) -> Produto:
        produto = self.buscar(produto_id)

        existente = self.repo.buscar_por_nome(dados.nome)
        if existente is not None and existente.id != produto.id:
            raise ProdutoJaExiste(dados.nome)

        produto.nome = dados.nome
        produto.preco = dados.preco
        produto.estoque = dados.estoque
        self.session.commit()
        return produto

    def apagar(self, produto_id: int) -> None:
        produto = self.buscar(produto_id)
        self.repo.remover(produto)
        self.session.commit()
