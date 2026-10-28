import numpy as np

diario = np.load("dados/processados/diario.npy")
usinas = np.array([diario[:64].sum(axis=0),
                   diario[64:110].sum(axis=0),
                   diario[110:].sum(axis=0)])
manter = np.ones(365, dtype=bool)
manter[345:348] = False
x = usinas[:, manter]
x = x - x.mean(axis=1, keepdims=True)
x /= np.linalg.norm(x, axis=1, keepdims=True)
print((x @ x.T).round(4))
