taxa = 0.12


def com_margem(preco):
    resultado = preco * (1 + taxa)
    return resultado


print(com_margem(8.90))
print(resultado)   # NameError
