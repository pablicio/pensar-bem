import numpy as np
from sklearn.linear_model import LogisticRegression

from risco.dados import tabela, treino_validacao

FINANCEIRAS = ["valor", "parcelas", "faturamento_declarado",
               "comprometimento", "atrasos_anteriores",
               "idade"]


def sigmoide(z):
    return 1 / (1 + np.exp(-z))


def perda_log(y, p):
    """A entropia cruzada média do volume 1."""
    return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))


treino, valid = treino_validacao(tabela())
media = treino[FINANCEIRAS].mean()
desvio = treino[FINANCEIRAS].std(ddof=0)
X = ((treino[FINANCEIRAS] - media) / desvio).to_numpy()
y = treino["alvo"].to_numpy()

# descida do gradiente, como no capítulo 19 do volume 1
w, b, passo = np.zeros(X.shape[1]), 0.0, 1.0
for volta in range(2_001):
    p = sigmoide(X @ w + b)
    if volta in (0, 10, 100, 1000, 2000):
        print(f"volta {volta:6,}: perda {perda_log(y, p):.4f}")
    w -= passo * X.T @ (p - y) / len(y)
    b -= passo * np.mean(p - y)

sk = LogisticRegression(C=np.inf, tol=1e-10, max_iter=10_000)
sk.fit(X, y)
print()
print("coluna                   à mão  scikit-learn")
for nome, a, s in zip(FINANCEIRAS, w, sk.coef_[0]):
    print(f"{nome:22} {a:7.4f} {s:13.4f}")
print(f"{'intercepto':22} {b:7.4f} {sk.intercept_[0]:13.4f}")
