from fastapi import APIRouter

router = APIRouter(prefix="/produtos", tags=["produtos"])


@router.get("")
def listar():
    return []


@router.get("/{produto_id}")
def buscar(produto_id: int):
    return {"id": produto_id}
