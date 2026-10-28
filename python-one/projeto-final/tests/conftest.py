import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_produto_servico
from app.main import app
from tests.dubles import RepositorioFalso, SessaoFalsa


@pytest.fixture
def servico_falso():
    return ProdutoServico(SessaoFalsa(), RepositorioFalso())


@pytest.fixture
def cliente(servico_falso):
    app.dependency_overrides[get_produto_servico] = (
        lambda: servico_falso
    )
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
