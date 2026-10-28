from typing import Annotated

from fastapi import Query


@router.get("", response_model=Pagina[ProdutoLer])
def listar(
    servico: ServicoDep,
    pagina: Annotated[int, Query(ge=1)] = 1,
    tamanho: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return servico.listar(pagina=pagina, tamanho=tamanho)
