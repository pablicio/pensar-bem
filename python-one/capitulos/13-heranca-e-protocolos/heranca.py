class Item:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    def etiqueta(self):
        return f"{self.nome} — R$ {self.preco:.2f}"


class ItemPesavel(Item):
    def __init__(self, nome, preco_kg, peso_kg):
        super().__init__(nome, preco_kg)
        self.peso_kg = peso_kg

    def etiqueta(self):
        base = super().etiqueta()
        return f"{base}/kg · {self.peso_kg} kg"
