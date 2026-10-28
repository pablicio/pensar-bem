from informacao import entropia_cruzada
from previsoes import CLIENTES, contagem, groove

ocorridos = [real for _, real in CLIENTES]
sistemas = [("Groove", groove), ("contagem", contagem)]
for nome, sistema in sistemas:
    previsoes = [sistema(h) for h, _ in CLIENTES]
    acertos = sum(1 for q, real in zip(previsoes, ocorridos)
                  if q.index(max(q)) == real)
    h = entropia_cruzada(previsoes, ocorridos)
    print(f"{nome:9} acertos {acertos} de {len(ocorridos)}, "
          f"entropia cruzada {h:.3f} bits")
