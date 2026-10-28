def alterar(self, produto_id: int, campos: dict) -> Produto:
    produto = self.buscar(produto_id)

    for campo, valor in campos.items():
        setattr(produto, campo, valor)

    self.session.commit()
    return produto
