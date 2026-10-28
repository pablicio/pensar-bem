def preco_justo(nota):
    # regra do Beto: nota 5 vale R$ 45 e nota 10 vale R$ 120
    a = (120 - 45) / (10 - 5)
    b = 45 - a * 5
    return a * nota + b
