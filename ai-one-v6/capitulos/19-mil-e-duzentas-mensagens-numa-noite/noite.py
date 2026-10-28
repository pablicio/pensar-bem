import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from rio.texto import CLASSES, mensagens

tab = mensagens()
noite = tab[(tab["data_hora"] >= "2026-10-14 19:00")
            & (tab["data_hora"] < "2026-10-15 07:00")]
print("mensagens das 19h às 7h:", len(noite))
print(noite["verdade"].value_counts()[CLASSES].to_string())
ivone = noite[noite["texto"].str.endswith("ivone")].iloc[0]
antes = (noite["data_hora"] < ivone["data_hora"]).sum()
print(f"a da Dona Ivone chegou às {ivone['data_hora']:%H:%M},"
      f" depois de {antes} outras")
por_hora = noite.groupby(
    [noite["data_hora"].dt.floor("h"), "verdade"]).size()
por_hora = por_hora.unstack(fill_value=0)[CLASSES]
fig, ax = plt.subplots(figsize=(7, 3))
por_hora.plot.bar(stacked=True, ax=ax, width=0.85,
                  color=["#b22", "#e93", "#999", "#58a"])
ax.set_xticklabels([f"{h:%Hh}" for h in por_hora.index],
                   rotation=0)
ax.set_xlabel("")
ax.set_ylabel("mensagens por hora")
fig.tight_layout()
fig.savefig("noite.png", dpi=300)
