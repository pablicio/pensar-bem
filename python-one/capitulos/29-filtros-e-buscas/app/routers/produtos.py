@router.get("", response_model=Pagina[ProdutoLer])
def listar(
    servico: ServicoDep,
    filtro: Annotated[ProdutoFiltro, Query()],
    pagina: Annotated[int, Query(ge=1)] = 1,
    tamanho: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return servico.listar(filtro, pagina, tamanho)
