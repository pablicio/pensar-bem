from fastapi import APIRouter

router = APIRouter(prefix="/produtos", tags=["produtos"])

_catalogo: list[dict] = [
    {"id": 1, "nome": "Tomate italiano",
     "preco": 8.90, "estoque": 120},
    {"id": 2, "nome": "Alface crespa",
     "preco": 3.50, "estoque": 40},
]
_proximo_id = 3
