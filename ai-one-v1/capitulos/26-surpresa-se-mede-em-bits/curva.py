import matplotlib.pyplot as plt

from informacao import surpresa

ps = [i / 200 for i in range(1, 201)]
plt.figure(figsize=(6, 3.5))
plt.plot(ps, [surpresa(p) for p in ps])
for p in [0.94, 0.5, 0.02]:
    plt.plot(p, surpresa(p), marker="o", color="black")
plt.xlabel("chance dada ao que aconteceu")
plt.ylabel("surpresa (bits)")
plt.savefig("surpresa.png", dpi=300, bbox_inches="tight")
