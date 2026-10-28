from sqlalchemy.exc import IntegrityError


def test_nome_duplicado_viola_restricao(session):
    session.add(Produto(nome="Tomate", preco=Decimal("8.90")))
    session.flush()

    session.add(Produto(nome="Tomate", preco=Decimal("9.10")))

    with pytest.raises(IntegrityError):
        session.flush()


def test_estoque_negativo_e_recusado(session):
    produto = Produto(
        nome="Tomate", preco=Decimal("8.90"), estoque=0
    )
    session.add(produto)
    session.flush()

    produto.estoque = -1

    with pytest.raises(IntegrityError):
        session.flush()


def test_preco_mantem_duas_casas(session):
    session.add(
        Produto(nome="Tomate", preco=Decimal("8.905"))
    )
    session.flush()
    session.expire_all()

    lido = session.scalars(select(Produto)).one()
    assert lido.preco == Decimal("8.91")
