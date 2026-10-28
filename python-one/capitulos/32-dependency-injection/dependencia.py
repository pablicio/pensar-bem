from typing import Annotated

from fastapi import Depends


def paginacao(pagina: int = 1, tamanho: int = 20) -> dict:
    return {
        "pagina": max(1, pagina),
        "tamanho": max(1, min(tamanho, 100)),
    }


PaginacaoDep = Annotated[dict, Depends(paginacao)]


@router.get("")
def listar(servico: ServicoDep, pag: PaginacaoDep):
    return servico.listar(**pag)
