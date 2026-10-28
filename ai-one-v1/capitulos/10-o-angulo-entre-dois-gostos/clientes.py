def ler_clientes(caminho):
    nomes = []
    compras = []
    with open(caminho, encoding="utf-8") as arquivo:
        arquivo.readline()
        for linha in arquivo:
            campos = linha.strip().split(",")
            nomes.append(campos[0])
            vetor = []
            for texto in campos[1:]:
                vetor.append(int(texto))
            compras.append(vetor)
    return nomes, compras
