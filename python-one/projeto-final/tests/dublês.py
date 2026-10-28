class RepositorioFalso:
    def __init__(self, inicial: list[Produto] | None = None):
        self._dados: dict[int, Produto] = {}
        self._proximo = 1
        for p in inicial or []:
            self.criar(p)

    def buscar(self, produto_id: int) -> Produto | None:
        return self._dados.get(produto_id)

    def buscar_por_nome(self, nome: str) -> Produto | None:
        for p in self._dados.values():
            if p.nome == nome:
                return p
        return None

    def listar(self, limite=20, deslocamento=0) -> list[Produto]:
        todos = sorted(self._dados.values(), key=lambda p: p.nome)
        return todos[deslocamento : deslocamento + limite]

    def criar(self, produto: Produto) -> Produto:
        produto.id = self._proximo
        self._dados[produto.id] = produto
        self._proximo += 1
        return produto

    def remover(self, produto: Produto) -> None:
        self._dados.pop(produto.id, None)
