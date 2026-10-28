def test_criar_sem_token_devolve_401(cliente):
    resposta = cliente.post(
        "/produtos", json={"nome": "Tomate", "preco": "8.90"}
    )

    assert resposta.status_code == 401


def test_produtor_nao_apaga_produto(cliente, usuario_produtor):
    app.dependency_overrides[usuario_atual] = (
        lambda: usuario_produtor
    )

    resposta = cliente.delete("/produtos/1")

    assert resposta.status_code == 403
