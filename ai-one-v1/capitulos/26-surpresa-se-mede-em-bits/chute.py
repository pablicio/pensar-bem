from informacao import entropia_cruzada
from previsoes import CLIENTES

ocorridos = [real for _, real in CLIENTES]
previsoes = [[0.25, 0.25, 0.25, 0.25] for _ in CLIENTES]
acertos = sum(1 for q, real in zip(previsoes, ocorridos)
              if q.index(max(q)) == real)
h = entropia_cruzada(previsoes, ocorridos)
print(f"acertos {acertos}, entropia cruzada {h:.3f} bits")
