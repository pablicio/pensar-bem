class SessaoFalsa:
    def __init__(self):
        self.commits = 0
        self.rollbacks = 0

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


@pytest.fixture
def servico():
    return ProdutoServico(SessaoFalsa(), RepositorioFalso())
