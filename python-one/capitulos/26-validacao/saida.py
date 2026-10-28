@router.get("/{produto_id}", response_model=ProdutoLer)
def buscar(produto_id: int, servico: ServicoDep):
    return servico.buscar(produto_id)
