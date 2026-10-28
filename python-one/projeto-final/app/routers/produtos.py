from fastapi import APIRouter, HTTPException, status

from app.dependencies import ServicoDep
from app.schemas.produto import ProdutoCriar, ProdutoLer
from app.services.produto import (
    EstoqueInsuficiente,
    ProdutoJaExiste,
    ProdutoNaoEncontrado,
)

router = APIRouter(prefix="/produtos", tags=["produtos"])


@router.get("", response_model=list[ProdutoLer])
def listar(servico: ServicoDep, limite: int = 20, pagina: int = 1):
    return servico.listar(limite=limite, pagina=pagina)


@router.get("/{produto_id}", response_model=ProdutoLer)
def buscar(produto_id: int, servico: ServicoDep):
    try:
        return servico.buscar(produto_id)
    except ProdutoNaoEncontrado as erro:
        raise HTTPException(404, str(erro)) from erro


@router.post(
    "", response_model=ProdutoLer, status_code=status.HTTP_201_CREATED
)
def criar(dados: ProdutoCriar, servico: ServicoDep):
    try:
        return servico.criar(
            dados.nome, dados.preco, dados.estoque
        )
    except ProdutoJaExiste as erro:
        raise HTTPException(409, str(erro)) from erro


@router.put("/{produto_id}", response_model=ProdutoLer)
def atualizar(
    produto_id: int, dados: ProdutoCriar, servico: ServicoDep
):
    try:
        return servico.atualizar(produto_id, dados)
    except ProdutoNaoEncontrado as erro:
        raise HTTPException(404, str(erro)) from erro
    except ProdutoJaExiste as erro:
        raise HTTPException(409, str(erro)) from erro


@router.delete("/{produto_id}", status_code=204)
def apagar(produto_id: int, servico: ServicoDep):
    try:
        servico.apagar(produto_id)
    except ProdutoNaoEncontrado as erro:
        raise HTTPException(404, str(erro)) from erro
