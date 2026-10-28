@router.post("", response_model=ProdutoLer, status_code=201)
def criar(
    dados: ProdutoCriar,
    servico: ServicoDep,
    usuario: UsuarioDep,
):
    return servico.criar(dados, criado_por=usuario.id)
