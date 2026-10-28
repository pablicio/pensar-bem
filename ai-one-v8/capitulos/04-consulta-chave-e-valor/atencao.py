import numpy as np
import torch
import torch.nn.functional as F

from lupa.atencao_numpy import atencao, softmax

np.set_printoptions(precision=4, suppress=True)
tokens = ["Prazo", "12", "Valor", "90.000"]
# dimensões: é rótulo, é número, fala de tempo, de dinheiro
K = np.array([[1, 0, 1, 0],
              [0, 1, 1, 0],
              [1, 0, 0, 1],
              [0, 1, 0, 1]], dtype=float)
# o conteúdo: meses e milhares de reais
V = np.array([[0, 0],
              [12, 0],
              [0, 0],
              [0, 90]], dtype=float)
# a consulta: "o número que fala de dinheiro"
q = np.array([[0, 2, 0, 2]], dtype=float)

notas = q @ K.T
print("q·k:     ", notas[0])
print("q·k / √4:", notas[0] / 2)
saida, pesos = atencao(q, K, V)
print("pesos:   ", pesos[0], f"soma {pesos.sum():.4f}")
print("saída:   ", saida[0])

# a mesma conta pela função do PyTorch
t = [torch.tensor(a, dtype=torch.float64) for a in (q, K, V)]
pt = F.scaled_dot_product_attention(*t)
print("PyTorch: ", pt.numpy()[0])

# a softmax ingênua estoura; a estável, não
z = np.array([1000.0, 1001.0, 1002.0])
with np.errstate(over="ignore", invalid="ignore"):
    print("\ningênua:", np.exp(z) / np.exp(z).sum())
print("estável:", softmax(z))
