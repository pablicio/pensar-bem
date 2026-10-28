import matplotlib.pyplot as plt

from lucro import lucro, receita

precos = [40 + 0.1 * k for k in range(1101)]  # R$ 40 a R$ 150
lucros = [lucro(p) for p in precos]
lucro_max, preco_max = max(zip(lucros, precos))
print(f"pela busca: R$ {preco_max:.2f},"
      f" lucro de R$ {lucro_max:.2f}")
for p in [69.90, 88.00, 89.90, 99.90]:
    print(f"  a R$ {p:6.2f}:"
          f" lucro de R$ {lucro(p):7.2f} por mês")

plt.figure(figsize=(6, 3.6))
plt.plot(precos, [receita(p) for p in precos], linestyle="--",
         label="receita")
plt.plot(precos, lucros, label="lucro")
plt.scatter([preco_max], [lucro_max])
plt.xlabel("preço da reedição (R$)")
plt.ylabel("R$ por mês")
plt.legend()
plt.savefig("lucro.png", dpi=300, bbox_inches="tight")
