import secrets

def exigir_api_key(x_api_key: Annotated[str | None, Header()] = None):
    esperada = get_config().api_key
    if x_api_key is None or not secrets.compare_digest(
        x_api_key, esperada
    ):
        raise HTTPException(401, "chave inválida")


@router.post("", dependencies=[Depends(exigir_api_key)])
def criar(dados: ProdutoCriar, servico: ServicoDep):
    ...
