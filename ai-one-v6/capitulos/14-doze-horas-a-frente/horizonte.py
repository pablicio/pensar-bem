import matplotlib.pyplot as plt
import numpy as np

from rio.avalia import mae, parte
from rio.serie import nivel_cidade

teste = parte(nivel_cidade(), "teste")
persistencia = [mae(teste.shift(h) - teste) * 100
                for h in range(1, 13)]
curvas = {"persistência": persistencia,
          "recursiva": np.load("recursiva.npy"),
          "direta": np.load("direta.npy"),
          "encoder-decoder": np.load("enc_dec.npy")}
horas = np.arange(1, 13)
fig, ax = plt.subplots(figsize=(6, 3.2))
for nome, erros in curvas.items():
    ax.plot(horas, erros, marker="o", ms=3, label=nome)
    print(f"{nome:16} 1 h {erros[0]:5.2f}"
          f"   6 h {erros[5]:5.2f}   12 h {erros[11]:5.2f}")
ax.set_xlabel("horizonte (horas)")
ax.set_ylabel("erro absoluto médio (cm)")
ax.set_xticks(horas)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("horizonte.png", dpi=300)
