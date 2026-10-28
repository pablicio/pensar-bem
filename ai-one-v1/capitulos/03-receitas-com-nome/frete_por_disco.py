import matplotlib.pyplot as plt

from frete import frete, peso_pacote

discos = list(range(1, 21))
por_disco = []
for n in discos:
    por_disco.append(frete(peso_pacote(n)) / n)

plt.figure(figsize=(6, 3.5))
plt.plot(discos, por_disco, marker="o", linestyle="none")
plt.xlabel("discos no pacote")
plt.ylabel("frete por disco (R$)")
plt.savefig("frete_por_disco.png", dpi=300,
            bbox_inches="tight")
for n in [7, 8, 12, 13]:
    print(n, round(por_disco[n - 1], 2))
