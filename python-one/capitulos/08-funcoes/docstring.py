def com_margem(preco, taxa=0.12):
    """Aplica a margem da cooperativa sobre o preço do produtor.

    O padrão de 12% vem do estatuto; produtos certificados usam 8%.
    """
    return preco * (1 + taxa)
