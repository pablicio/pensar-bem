cotas = [0.133, 1.3954, 0.099, 0.2591, 0.0405]
contagem = {"grande": 0, "média": 0, "pequena": 0}
for cota in cotas:
    if cota >= 1:
        contagem["grande"] += 1
    elif cota >= 0.2:
        contagem["média"] += 1
    else:
        contagem["pequena"] += 1
print(contagem)
