def registrar(produto, quantidade, *, conferido=False):
    ...


registrar("Tomate", 12, True)            # TypeError
registrar("Tomate", 12, conferido=True)  # ok
