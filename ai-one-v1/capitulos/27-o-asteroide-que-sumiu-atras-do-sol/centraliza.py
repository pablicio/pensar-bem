from minimos import descida, solucao_fechada
from vendidos import notas_e_precos

pares = notas_e_precos(2026, 200)
mx = sum(x for x, _ in pares) / len(pares)
centrados = [(x - mx, y) for x, y in pares]
af, bf = solucao_fechada(centrados)
print(f"fechada: a = {af:.3f}  b = {bf:.3f}")
for passos in [10, 20, 50, 100]:
    a, b, historico = descida(centrados, 0.1, passos)
    print(f"{passos:3} passos: a = {a:.3f}  b = {b:.3f}  "
          f"perda {historico[-1]:.2f}")
