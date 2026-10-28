TAXA = 0.12


def com_margem(preco, taxa=TAXA):
    return preco * (1 + taxa)


if __name__ == "__main__":
    print("teste:", com_margem(10))
