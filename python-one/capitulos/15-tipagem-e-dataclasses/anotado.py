def com_margem(preco: float, taxa: float = 0.12) -> float:
    return preco * (1 + taxa)


print(com_margem("oito reais"))
