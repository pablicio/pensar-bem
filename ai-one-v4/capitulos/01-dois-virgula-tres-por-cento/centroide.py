from collections import Counter

import numpy as np

from mnist import carregar

X, y = carregar("treino")
Xt, yt = carregar("teste")
# um vetor de 784 números de 0 a 1 por imagem
X = X.reshape(len(X), 784) / 255
Xt = Xt.reshape(len(Xt), 784) / 255

# o "dígito médio" de cada classe
centros = np.stack([X[y == d].mean(axis=0) for d in range(10)])
dif = Xt[:, None, :] - centros[None, :, :]
dist = (dif**2).sum(axis=2)
previsto = dist.argmin(axis=1)

print(f"acerto no teste: {(previsto == yt).mean():.1%}")
erros = Counter(zip(yt[previsto != yt].tolist(),
                    previsto[previsto != yt].tolist()))
print("as confusões mais comuns (era, leu, quantas):")
for (era, leu), n in erros.most_common(5):
    print(f"  {era} lido como {leu}: {n}")
