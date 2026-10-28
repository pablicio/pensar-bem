from demanda import demanda

p = 89.90
print("       h    para frente       centrada")
for h in [10, 1, 0.1, 0.01, 1e-3, 1e-5, 1e-8, 1e-11, 1e-13]:
    frente = (demanda(p + h) - demanda(p)) / h
    centrada = (demanda(p + h) - demanda(p - h)) / (2 * h)
    print(f"{h:8.0e}  {frente:13.10f}  {centrada:13.10f}")
