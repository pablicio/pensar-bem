class ErroDoCatalogo(Exception):
    """Base de todos os erros do domínio."""


class ProdutoNaoEncontrado(ErroDoCatalogo):
    def __init__(self, produto_id: int):
        self.produto_id = produto_id
        super().__init__(f"produto {produto_id} não encontrado")


class EstoqueInsuficiente(ErroDoCatalogo):
    def __init__(self, disponivel: int, pedido: int):
        self.disponivel = disponivel
        self.pedido = pedido
        super().__init__(
            f"estoque insuficiente: {disponivel} < {pedido}"
        )
