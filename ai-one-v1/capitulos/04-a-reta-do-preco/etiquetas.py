import matplotlib.pyplot as plt

from reta import preco_justo

# nota de estado (1 a 10) e preço marcado na etiqueta, em reais
notas = [4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10]
precos = [32, 45, 49, 58, 64, 89, 74, 70, 92, 104, 101, 118]

print("nota  etiqueta   reta  desvio")
for nota, preco in zip(notas, precos):
    reta = preco_justo(nota)
    desvio = preco - reta
    alerta = "  <-- confira" if abs(desvio) > 10 else ""
    print(f"{nota:4d}{preco:10d}{reta:7.1f}"
          f"{desvio:+8.1f}{alerta}")

plt.figure(figsize=(6, 3.5))
plt.scatter(notas, precos)
plt.plot([3.5, 10.5], [preco_justo(3.5), preco_justo(10.5)])
plt.xlabel("nota de estado")
plt.ylabel("preço na etiqueta (R$)")
plt.savefig("reta_preco.png", dpi=300, bbox_inches="tight")
