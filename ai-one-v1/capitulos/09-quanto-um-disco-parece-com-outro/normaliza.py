def normalizar(vetores):
    n = len(vetores[0])
    minimos = []
    maximos = []
    for i in range(n):
        coluna = []
        for v in vetores:
            coluna.append(v[i])
        minimos.append(min(coluna))
        maximos.append(max(coluna))
    normalizados = []
    for v in vetores:
        novo = []
        for i in range(n):
            amplitude = maximos[i] - minimos[i]
            novo.append((v[i] - minimos[i]) / amplitude)
        normalizados.append(novo)
    return normalizados, minimos, maximos
