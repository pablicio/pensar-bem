class ProdutoCriar(ProdutoBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "nome": "Tomate italiano",
                    "preco": "8.90",
                    "estoque": 120,
                }
            ]
        }
    )
