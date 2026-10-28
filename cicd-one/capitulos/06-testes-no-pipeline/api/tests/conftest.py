@pytest.fixture
def db(conexao):
    transacao = conexao.begin()
    yield conexao
    transacao.rollback()
