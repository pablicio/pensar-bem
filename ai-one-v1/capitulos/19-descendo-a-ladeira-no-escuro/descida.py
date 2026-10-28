import matplotlib.pyplot as plt


def erro(x):
    return (x - 3) ** 2


def derivada(x):
    return 2 * (x - 3)


plt.figure(figsize=(6, 3.5))
for eta, estilo in [(0.1, "-"), (1.1, "--")]:
    x = 0.0
    erros = []
    for passo in range(1, 21):
        x = x - eta * derivada(x)
        erros.append(erro(x))
        if passo <= 4 or passo == 20:
            print(f"eta {eta}  passo {passo:2d}  x = {x:10.4f}"
                  f"  erro = {erro(x):12.4f}")
    plt.plot(range(1, 21), erros, linestyle=estilo,
             label=f"η = {eta}")
plt.yscale("log")
plt.xlabel("passo")
plt.ylabel("erro (escala log)")
plt.legend()
plt.savefig("descida.png", dpi=300, bbox_inches="tight")
