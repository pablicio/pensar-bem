import numpy as np

gerador = np.random.default_rng(2027_04)
sorteados = gerador.choice(140, size=10, replace=False)
escolhidos = np.sort(sorteados)
resto = np.where(escolhidos < 110, "Cocalzinho", "Abadiânia")
usina = np.where(escolhidos < 64, "Corumbá", resto)
for numero, nome in zip(escolhidos, usina):
    print(int(numero), nome)
