def test_criar_devolve_201_e_o_recurso(cliente):
    resposta = cliente.post(
        "/produtos",
        json={"nome": "Tomate", "preco": "8.90", "estoque": 10},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["id"] > 0
    assert corpo["nome"] == "Tomate"
    assert "senha" not in corpo


def test_buscar_inexistente_devolve_404(cliente):
    resposta = cliente.get("/produtos/999")

    assert resposta.status_code == 404
    assert resposta.json()["tipo"] == "produto_nao_encontrado"


def test_nome_repetido_devolve_409(cliente):
    dados = {"nome": "Tomate", "preco": "8.90"}
    cliente.post("/produtos", json=dados)

    resposta = cliente.post("/produtos", json=dados)

    assert resposta.status_code == 409


def test_preco_negativo_devolve_422(cliente):
    resposta = cliente.post(
        "/produtos", json={"nome": "Tomate", "preco": "-1"}
    )

    assert resposta.status_code == 422
    campos = resposta.json()["campos"]
    assert any(c["campo"] == "preco" for c in campos)
