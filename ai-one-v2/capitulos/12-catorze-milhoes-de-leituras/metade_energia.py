import numpy as np

energia = np.load("dados/processados/leituras_ano.npy")
b = energia[64:110].ravel()
b = np.sort(b[b > 0])[::-1]            # do maior para o menor
acumulada = np.cumsum(b)
metade = np.searchsorted(acumulada, acumulada[-1] / 2)
print(f"{b.size} intervalos com geração")
print(f"metade da energia em {metade} deles: "
      f"{metade / b.size:.1%}")
