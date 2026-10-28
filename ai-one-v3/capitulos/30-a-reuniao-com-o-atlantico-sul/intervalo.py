import numpy as np

from politicas import politicas

teste, valores, regras = politicas()
jussara, _, modelo, _ = regras.values()
sorteio = np.random.default_rng(0)
diferencas = []
for _ in range(1_000):
    i = sorteio.integers(0, len(valores), len(valores))
    diferencas.append(valores[i][modelo[i]].sum()
                      - valores[i][jussara[i]].sum())
baixo, meio, alto = np.percentile(diferencas, [2.5, 50, 97.5])
print(f"lucro a mais do modelo: {meio:,.0f}"
      f" (95% entre {baixo:,.0f} e {alto:,.0f})")
print(f"reamostragens em que o modelo perde: "
      f"{np.mean(np.array(diferencas) < 0):.1%}")
