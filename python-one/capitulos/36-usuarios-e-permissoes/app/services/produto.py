def atualizar(
    self, produto_id: int, dados: ProdutoAtualizar,
    usuario: Usuario,
) -> Produto:
    produto = self.buscar(produto_id)

    if usuario.papel is Papel.PRODUTOR:
        if produto.produtor_id != usuario.produtor_id:
            raise SemPermissao(produto_id)

    alteracoes = dados.model_dump(exclude_unset=True)
    for campo, valor in alteracoes.items():
        setattr(produto, campo, valor)

    self.session.commit()
    return produto
