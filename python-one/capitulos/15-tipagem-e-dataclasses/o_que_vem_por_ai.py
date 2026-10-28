@app.get("/produtos/{produto_id}")
def buscar(
    produto_id: int, incluir_inativos: bool = False
) -> Produto:
    ...
