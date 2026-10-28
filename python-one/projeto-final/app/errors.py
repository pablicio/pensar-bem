from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.services.produto import (
    EstoqueInsuficiente,
    ProdutoJaExiste,
    ProdutoNaoEncontrado,
)


def registrar_tratadores(app: FastAPI) -> None:

    @app.exception_handler(ProdutoNaoEncontrado)
    async def _nao_encontrado(
        request: Request, exc: ProdutoNaoEncontrado
    ):
        return JSONResponse(
            status_code=404,
            content={
                "tipo": "produto_nao_encontrado",
                "mensagem": str(exc),
                "recurso_id": exc.produto_id,
            },
        )

    @app.exception_handler(ProdutoJaExiste)
    async def _ja_existe(request: Request, exc: ProdutoJaExiste):
        return JSONResponse(
            status_code=409,
            content={
                "tipo": "produto_ja_existe",
                "mensagem": str(exc),
                "nome": exc.nome,
            },
        )

    @app.exception_handler(EstoqueInsuficiente)
    async def _estoque(
        request: Request, exc: EstoqueInsuficiente
    ):
        return JSONResponse(
            status_code=409,
            content={
                "tipo": "estoque_insuficiente",
                "mensagem": str(exc),
                "disponivel": exc.disponivel,
                "pedido": exc.pedido,
            },
        )
