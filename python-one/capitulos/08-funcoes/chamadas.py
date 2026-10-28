def registrar(produto, quantidade, conferido=False):
    ...


registrar("Tomate", 12)
registrar("Tomate", 12, True)
registrar("Tomate", quantidade=12, conferido=True)
registrar(quantidade=12, produto="Tomate")
