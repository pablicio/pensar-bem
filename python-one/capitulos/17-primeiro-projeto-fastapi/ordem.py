@router.get("/{produto_id}")
def buscar(produto_id: int):
    ...


@router.get("/destaques")     # nunca é alcançada
def destaques():
    ...
