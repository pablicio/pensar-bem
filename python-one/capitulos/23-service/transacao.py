def transferir(self, de_id: int, para_id: int, caixas: int) -> None:
    origem = self.repo.buscar(de_id)
    destino = self.repo.buscar(para_id)

    if origem is None:
        raise ProdutoNaoEncontrado(de_id)
    if destino is None:
        raise ProdutoNaoEncontrado(para_id)
    if origem.estoque < caixas:
        raise EstoqueInsuficiente(origem.estoque, caixas)

    origem.estoque -= caixas
    destino.estoque += caixas
    self.session.commit()
