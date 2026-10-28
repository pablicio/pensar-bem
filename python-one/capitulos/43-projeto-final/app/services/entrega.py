def conferir(
    self, entrega_id: int, itens: dict[int, int],
    usuario: Usuario,
) -> Entrega:
    entrega = self.session.get(
      Entrega, entrega_id, with_for_update=True
    )
    if entrega is None:
      raise EntregaNaoEncontrada(entrega_id)

    if entrega.status is not StatusEntrega.PENDENTE:
        raise EntregaJaFinalizada(entrega.id, entrega.status)

    for item in entrega.itens:
        if item.id not in itens:
            raise ItemNaoConferido(item.id)
        item.caixas_conferidas = itens[item.id]

    for item in entrega.itens:
        produto = self.repo_produto.buscar(item.produto_id)
        produto.estoque += item.caixas_conferidas

    entrega.status = StatusEntrega.CONFERIDA
    entrega.conferida_por = usuario.id
    entrega.conferida_em = datetime.now(timezone.utc)

    self.session.commit()
    return entrega
