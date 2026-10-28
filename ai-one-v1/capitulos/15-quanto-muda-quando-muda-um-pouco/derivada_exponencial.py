from demanda import demanda

h = 0.001
for p in [60, 89.90, 120]:
    numerica = (demanda(p + h) - demanda(p - h)) / (2 * h)
    exata = -0.02 * demanda(p)
    print(f"{p:6.2f}  {numerica:.6f}  {exata:.6f}")
