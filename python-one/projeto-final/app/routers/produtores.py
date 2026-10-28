from fastapi import APIRouter

router = APIRouter(prefix="/produtores", tags=["produtores"])


@router.get("")
def listar():
    return []
