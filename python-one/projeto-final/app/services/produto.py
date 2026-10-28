from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.repositories.produto import ProdutoRepositorio


class ProdutoJaExiste(Exception):
    def __init__(self, nome: str):
        self.nome = nome
        super().__init__(f"produto '{nome}' já cadastrado")


class ProdutoNaoEncontrado(Exception):
    def __init__(self, produto_id: int):
        self.produto_id = produto_id
        super().__init__(f"produto {produto_id} não encontrado")


class EstoqueInsuficiente(Exception):
    def __init__(self, disponivel: int, pedido: int):
        self.disponivel = disponivel
        self.pedido = pedido
        super().__init__("estoque insuficiente")


class QuantidadeInvalida(Exception):
    def __init__(self, quantidade: int):
        self.quantidade = quantidade
        super().__init__("a quantidade deve ser maior que zero")


class ProdutoServico:
    def __init__(self, session: Session, repo: ProdutoRepositorio):
        self.session = session
        self.repo = repo

    def criar(
        self, nome: str, preco: Decimal, estoque: int
    ) -> Produto:
        nome = " ".join(nome.split())

        if self.repo.buscar_por_nome(nome) is not None:
            raise ProdutoJaExiste(nome)

        produto = Produto(nome=nome, preco=preco, estoque=estoque)
        self.repo.criar(produto)
        self.session.commit()
        return produto

    def vender(self, produto_id: int, quantidade: int) -> Produto:
        if quantidade <= 0:
            raise QuantidadeInvalida(quantidade)

        produto = self.repo.buscar(produto_id)
        if produto is None:
            raise ProdutoNaoEncontrado(produto_id)

        if quantidade > produto.estoque:
            raise EstoqueInsuficiente(produto.estoque, quantidade)

        produto.estoque -= quantidade
        self.session.commit()
        return produto
