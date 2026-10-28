@router.post(
    "",
    response_model=ProdutoLer,
    status_code=201,
    summary="Cadastra um produto",
    response_description="Produto criado, com identificador",
    responses={
        409: {
            "description": "Já existe produto com esse nome",
            "content": {
                "application/json": {
                    "example": {
                        "tipo": "produto_ja_existe",
                        "mensagem": "produto 'Tomate' já cadastrado",
                    }
                }
            },
        },
        422: {"description": "Campos inválidos"},
    },
)
def criar(dados: ProdutoCriar, servico: ServicoDep):
    """
    Cadastra um produto no catálogo.

    O nome é normalizado — espaços das pontas e espaços
    repetidos no meio são removidos — antes da verificação
    de duplicidade.
    """
    return servico.criar(dados)
