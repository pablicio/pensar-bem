def test_fluxo_completo_de_login(cliente_com_banco):
    cliente_com_banco.post(
        "/usuarios",
        json={
            "nome": "Bia",
            "email": "bia@sabia.coop",
            "senha": "segredo123",
        },
    )

    login = cliente_com_banco.post(
        "/auth/login",
        data={
            "username": "bia@sabia.coop",
            "password": "segredo123",
        },
    )
    token = login.json()["access_token"]

    resposta = cliente_com_banco.get(
        "/produtos",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resposta.status_code == 200
