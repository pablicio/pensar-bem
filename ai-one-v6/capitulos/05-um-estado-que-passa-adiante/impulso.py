import numpy as np

from rio.numpy_rnn import rnn, rnn_inicia

pulso = np.zeros((73, 1))
pulso[0] = 1.0                   # uma chuva só, na hora zero
print("W_h         depois de 1 h   6 h   24 h   72 h")
for a in (0.5, 0.9, 0.99):
    p = rnn_inicia(1, 4, np.random.default_rng(0))
    p["Wh"] = a * np.eye(4)  # cada unidade guarda a fração a
    norma = np.linalg.norm(rnn(p, pulso), axis=1)
    print(f"{a:4.2f} I    " + "  ".join(
        f"{norma[k]:6.3f}" for k in (1, 6, 24, 72)))
