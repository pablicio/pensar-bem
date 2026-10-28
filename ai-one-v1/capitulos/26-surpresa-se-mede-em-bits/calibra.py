from informacao import entropia_cruzada
from previsoes import CLIENTES

ocorridos = [real for _, real in CLIENTES]


def groove_com(c, historico):
    chute = historico.index(max(historico))
    return [c if g == chute else (1 - c) / 3 for g in range(4)]


for i in range(10, 20):
    c = i / 20
    previsoes = [groove_com(c, h) for h, _ in CLIENTES]
    h = entropia_cruzada(previsoes, ocorridos)
    print(f"c = {c:.2f}: {h:.3f} bits")
