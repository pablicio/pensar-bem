from collections import Counter

from lupa.busca import busca, palavras_chave
from lupa.diario import atos, gabarito, mostra

palavras = palavras_chave()
janeiro = [a for a in atos() if a["data"] >= "2027-01-01"]
achados = busca(janeiro, palavras)
print(len(palavras), "palavras-chave;", len(janeiro),
      "atos em janeiro;", len(achados), "achados")

# a Patrícia lê os achados
verdade = gabarito()
bons = [a for a, _ in achados if verdade[a["id"]]["relevante"]]
print(f"interessam à Cerrado Forte: {len(bons)}"
      f" ({len(bons) / len(achados):.0%})")
print("os outros, pela palavra que casou:")
outros = Counter(p for a, p in achados
                 if not verdade[a["id"]]["relevante"])
for p, n in outros.most_common(6):
    print(f"  {n:3}  {p}")

nova = [a for a in janeiro if "eixo central" in a["texto"]][0]
print("\nachou a de Nova Esperança?",
      any(a is nova for a, _ in achados))
mostra(nova["texto"])
