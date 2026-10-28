from sqlalchemy.exc import IntegrityError

try:
    self.repo.criar(produto)
    self.session.commit()
except IntegrityError as erro:
    self.session.rollback()
    raise ProdutoJaExiste(nome) from erro
