@router.post("", response_model=ProdutoLer, status_code=201)
def criar(
    dados: ProdutoCriar,
    servico: ProdutoServico = Depends(get_produto_servico),
):
    try:
        return servico.criar(dados.nome, dados.preco, dados.estoque)
    except ProdutoJaExiste as erro:
        raise HTTPException(409, str(erro)) from erro
