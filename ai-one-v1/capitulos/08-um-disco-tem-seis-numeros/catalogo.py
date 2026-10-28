def ler_catalogo(caminho):
    titulos = []
    vetores = []
    with open(caminho, encoding="utf-8") as arquivo:
        arquivo.readline()                  # pula o cabeçalho
        for linha in arquivo:
            campos = linha.strip().split(",")
            titulos.append(campos[1])
            vetor = []
            for texto in campos[2:]:
                vetor.append(float(texto))
            vetores.append(vetor)
    return titulos, vetores
