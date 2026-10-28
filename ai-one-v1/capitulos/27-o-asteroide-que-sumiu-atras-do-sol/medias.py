from minimos import solucao_fechada
from vendidos import notas_e_precos

pares = notas_e_precos(2026, 200)
a, b = solucao_fechada(pares)
mx = sum(x for x, _ in pares) / len(pares)
my = sum(y for _, y in pares) / len(pares)
print(f"médias: nota {mx:.3f}, preço {my:.3f}")
print(f"reta na nota média: {a * mx + b:.3f}")
