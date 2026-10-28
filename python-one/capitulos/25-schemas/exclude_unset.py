@router.patch("/{produto_id}", response_model=ProdutoLer)
def alterar(
    produto_id: int, dados: ProdutoAtualizar, servico: ServicoDep
):
    campos = dados.model_dump(exclude_unset=True)
    return servico.alterar(produto_id, campos)
