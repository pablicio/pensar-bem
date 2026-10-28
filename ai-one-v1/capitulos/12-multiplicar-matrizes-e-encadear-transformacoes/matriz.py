from similaridade import produto_escalar


def forma(A):
    return len(A), len(A[0])


def transposta(A):
    linhas, colunas = forma(A)
    T = []
    for j in range(colunas):
        nova = []
        for i in range(linhas):
            nova.append(A[i][j])
        T.append(nova)
    return T


def matriz_vezes_vetor(A, x):
    resultado = []
    for linha in A:
        resultado.append(produto_escalar(linha, x))
    return resultado


def multiplicar(A, B):
    Bt = transposta(B)
    resultado = []
    for linha in A:
        nova = []
        for coluna in Bt:
            nova.append(produto_escalar(linha, coluna))
        resultado.append(nova)
    return resultado
