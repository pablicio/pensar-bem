import matplotlib.pyplot as plt
import numpy as np

from rio.avalia import parte
from rio.entradas import tabela

tab = parte(tabela(), "treino")
subida = tab["cidade"].diff()
atrasos = np.arange(0, 25)
fig, ax = plt.subplots(figsize=(6, 3.2))
print("série               atraso   correlação")
for coluna in tab.columns[1:]:
    serie = tab[coluna]
    if not coluna.startswith("chuva"):
        serie = serie.diff()         # nível: a subida
    cc = [subida.corr(serie.shift(k)) for k in atrasos]
    k = int(np.argmax(cc))
    print(f"{coluna:18} {k:6d} h {cc[k]:10.3f}")
    ax.plot(atrasos, cc, label=coluna)
ax.set_xlabel("atraso (horas)")
ax.set_ylabel("correlação com a subida na cidade")
ax.legend(fontsize=7, ncol=2)
fig.tight_layout()
fig.savefig("correlacao.png", dpi=300)
