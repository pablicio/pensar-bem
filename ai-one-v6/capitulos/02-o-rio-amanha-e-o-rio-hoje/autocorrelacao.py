import matplotlib.pyplot as plt
import pandas as pd

from rio.avalia import parte

cadernos = pd.read_csv("dados/brutos/cadernos.csv",
                       parse_dates=["data_hora"],
                       index_col="data_hora")
nivel = cadernos["leitura_cm"].loc["1996-07-01":] / 100
nivel = parte(nivel[nivel < 14].asfreq("h"), "treino")
subida = nivel.diff()
atrasos = range(0, 73)
acf_nivel = [nivel.autocorr(k) for k in atrasos]
acf_subida = [subida.autocorr(k) for k in atrasos]
for k in (1, 6, 12, 24, 72):
    print(f"atraso {k:2d} h: nível {acf_nivel[k]:.3f}"
          f"   subida {acf_subida[k]:6.3f}")

fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(atrasos, acf_nivel, label="nível", color="#2A5F9E")
ax.plot(atrasos, acf_subida, label="subida de uma hora",
        color="#C0392B")
ax.axhline(0, color="0.6", lw=0.8)
ax.set_xlabel("atraso (horas)")
ax.set_ylabel("autocorrelação")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("autocorrelacao.png", dpi=300)
