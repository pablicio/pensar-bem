from app.main import app
from app.dependencies import get_session


def session_de_teste():
    with SessionTeste() as s:
        yield s


app.dependency_overrides[get_session] = session_de_teste
