import matplotlib.pyplot as plt

# compras de frevo (eixo x) e de rock (eixo y)
clientes = [("Dona Lindalva", (3, 0), "-"),
            ("Beto", (15, 0), "--"),
            ("Jorge", (1, 1), ":"),
            ("Rafael", (0, 12), "-.")]

plt.figure(figsize=(5.5, 5.5))
for nome, ponta, estilo in clientes:
    plt.annotate("", xy=ponta, xytext=(0, 0),
                 arrowprops={"arrowstyle": "->",
                             "linestyle": estilo})
    plt.text(ponta[0] + 0.3, ponta[1] + 0.3, nome)
plt.xlim(-1, 17)
plt.ylim(-1, 14)
plt.xlabel("discos de frevo")
plt.ylabel("discos de rock")
plt.savefig("angulos.png", dpi=300, bbox_inches="tight")
