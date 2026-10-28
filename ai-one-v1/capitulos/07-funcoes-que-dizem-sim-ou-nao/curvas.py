import matplotlib.pyplot as plt

from sigmoide import degrau, sigmoide

zs = []
for i in range(-60, 61):
    zs.append(i / 10)

plt.figure(figsize=(6, 5))
plt.subplot(2, 1, 1)
degraus = []
sigmoides = []
for z in zs:
    degraus.append(degrau(z))
    sigmoides.append(sigmoide(z))
plt.step(zs, degraus, where="post", linestyle="--",
         label="degrau")
plt.plot(zs, sigmoides, label="sigmoide")
plt.ylabel("saída")
plt.legend()

plt.subplot(2, 1, 2)
for a, estilo in [(0.5, ":"), (1, "-"), (3, "--")]:
    ys = []
    for z in zs:
        ys.append(sigmoide(a * z))
    plt.plot(zs, ys, linestyle=estilo, label=f"a = {a}")
plt.xlabel("z")
plt.ylabel("sigmoide(a z)")
plt.legend()
plt.savefig("sigmoide.png", dpi=300, bbox_inches="tight")
print(len(zs), "valores de z, de", zs[0], "a", zs[-1])
