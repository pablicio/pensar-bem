import numpy as np

from mnist import carregar


def zeros_e_uns(parte):
    imagens, rotulos = carregar(parte)
    so = (rotulos == 0) | (rotulos == 1)
    X = imagens[so].reshape(-1, 784) / 255
    return X, (rotulos[so] == 1).astype(int)    # 1 para o "um"


X, y = zeros_e_uns("treino")
print(f"{len(X):,} zeros e uns no treino")
w, b = np.zeros(784), 0.0
for passada in range(1, 51):        # no máximo 50 passadas
    erros = 0
    for xi, yi in zip(X, y):
        previsto = 1 if xi @ w + b > 0 else 0    # o degrau
        if previsto != yi:          # só aprende quando erra
            w += (yi - previsto) * xi
            b += yi - previsto
            erros += 1
    print(f"passada {passada:2}: {erros:3} erros")
    if erros == 0:
        break

Xt, yt = zeros_e_uns("teste")
acerto = ((Xt @ w + b > 0).astype(int) == yt).mean()
print(f"\nno teste: {acerto:.2%} de {len(Xt):,}")
np.save("pesos.npy", np.append(w, b))
