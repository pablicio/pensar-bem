import pytest


@pytest.fixture
def produto():
    return Produto(
        nome="Tomate italiano",
        preco=Decimal("8.90"),
        estoque=100,
    )
