class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    def __eq__(self, outro):
        if not isinstance(outro, Produto):
            return NotImplemented
        return (self.nome, self.preco) == (outro.nome, outro.preco)

    def __hash__(self):
        return hash((self.nome, self.preco))
