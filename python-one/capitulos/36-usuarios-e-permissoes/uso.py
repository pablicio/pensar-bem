@router.post("", response_model=ProdutoLer, status_code=201)
def criar(dados: ProdutoCriar, servico: ServicoDep,
          usuario: OperacaoDep):
    return servico.criar(dados)


@router.delete("/{produto_id}", status_code=204)
def apagar(produto_id: int, servico: ServicoDep,
           usuario: AdminDep):
    servico.apagar(produto_id)
