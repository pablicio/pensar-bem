class Produto:
    def __init__(self):
        self.__segredo = 42


p = Produto()
print(p.__segredo)      # AttributeError
print(p._Produto__segredo)   # 42
