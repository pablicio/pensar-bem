def test_openapi_tem_as_rotas_esperadas(cliente):
    esquema = cliente.get("/openapi.json").json()
    caminhos = esquema["paths"]

    assert "/produtos" in caminhos
    assert "get" in caminhos["/produtos"]
    assert "post" in caminhos["/produtos"]


def test_resposta_de_produto_nao_expoe_custo(cliente):
    esquema = cliente.get("/openapi.json").json()
    modelo = esquema["components"]["schemas"]["ProdutoLer"]

    assert "custo" not in modelo["properties"]
