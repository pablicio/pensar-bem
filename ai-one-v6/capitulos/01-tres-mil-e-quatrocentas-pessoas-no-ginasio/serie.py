import matplotlib.pyplot as plt
import pandas as pd

cadernos = pd.read_csv("dados/brutos/cadernos.csv",
                       parse_dates=["data_hora"],
                       index_col="data_hora")
nivel = cadernos["leitura_cm"] / 100
COTAS = {"atenção": 4.0, "alerta": 5.5, "inundação": 7.0}
JANELAS = [("outubro de 2026", "2026-10-13", "2026-10-17"),
           ("novembro de 2008", "2008-11-12", "2008-11-30")]

fig, eixos = plt.subplots(1, 2, figsize=(9, 3.4), sharey=True)
for ax, (titulo, inicio, fim) in zip(eixos, JANELAS):
    trecho = nivel.loc[inicio:fim]
    ax.plot(trecho.index, trecho, color="#2A5F9E", lw=1.4)
    for nome, cota in COTAS.items():
        ax.axhline(cota, color="0.5", lw=0.8, ls="--")
        ax.text(trecho.index[0], cota + 0.12, nome, fontsize=7,
                color="0.35")
    ax.set_title(titulo, fontsize=9)
    ax.tick_params(axis="x", labelsize=7, rotation=30)
    menor, maior = trecho.min(), trecho.max()
    print(f"{titulo}: de {menor:.2f} a {maior:.2f} m,"
          f" pico em {trecho.idxmax():%d/%m %Hh}")
eixos[0].set_ylabel("nível na régua (m)")
fig.tight_layout()
fig.savefig("serie.png", dpi=300)
