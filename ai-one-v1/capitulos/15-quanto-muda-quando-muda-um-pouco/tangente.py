import matplotlib.pyplot as plt

from demanda import demanda

p0, p1 = 89.90, 99.90
media = (demanda(p1) - demanda(p0)) / (p1 - p0)
h = 0.001
instantanea = (demanda(p0 + h) - demanda(p0 - h)) / (2 * h)


def reta(p, inclinacao):
    # a reta por (p0, demanda(p0)) com essa inclinação
    return demanda(p0) + inclinacao * (p - p0)


precos = [40 + i for i in range(101)]
xs = [p0 - 30, p0 + 40]
plt.figure(figsize=(6, 3.8))
plt.plot(precos, [demanda(p) for p in precos], label="demanda")
plt.plot(xs, [reta(x, media) for x in xs], linestyle=":",
         label="secante (taxa média)")
plt.plot(xs, [reta(x, instantanea) for x in xs],
         linestyle="--", label="tangente (derivada)")
plt.scatter([p0, p1], [demanda(p0), demanda(p1)])
plt.xlabel("preço da reedição (R$)")
plt.ylabel("cópias por mês")
plt.legend()
plt.savefig("tangente.png", dpi=300, bbox_inches="tight")
print(f"taxa média de R$ {p0} a R$ {p1}: {media:.3f}"
      " cópias por real")
print(f"derivada em R$ {p0}: {instantanea:.3f}"
      " cópias por real")
