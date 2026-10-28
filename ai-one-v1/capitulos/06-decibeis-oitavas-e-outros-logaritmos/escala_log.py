import math

import matplotlib.pyplot as plt

v0 = 2400.0
taxa = (9000 / 2400) ** (1 / 7) - 1

anos = list(range(0, 21))
valores = []
logs = []
for t in anos:
    v = v0 * (1 + taxa) ** t
    valores.append(v)
    logs.append(math.log10(v))

for t in [0, 1, 2, 10, 20]:
    print(f"ano {t:2d}  valor {valores[t]:10.2f}"
          f"  log10 {logs[t]:.4f}")
print(f"cada ano soma {math.log10(1 + taxa):.4f} ao log10")

plt.figure(figsize=(6, 5))
plt.subplot(2, 1, 1)
plt.plot(anos, valores)
plt.ylabel("valor (R$)")
plt.subplot(2, 1, 2)
plt.plot(anos, valores)
plt.yscale("log")
plt.ylabel("valor (R$), escala log")
plt.xlabel("anos desde 2019")
plt.savefig("escala_log.png", dpi=300, bbox_inches="tight")
