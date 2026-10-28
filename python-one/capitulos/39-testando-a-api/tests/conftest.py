@pytest.fixture
def cliente_autenticado(cliente, usuario_falso):
    app.dependency_overrides[usuario_atual] = (
        lambda: usuario_falso
    )
    yield cliente
    app.dependency_overrides.pop(usuario_atual, None)
