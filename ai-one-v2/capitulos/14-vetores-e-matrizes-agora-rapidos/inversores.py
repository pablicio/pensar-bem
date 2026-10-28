import numpy as np

diario = np.load("dados/processados/diario.npy")
normas = np.linalg.norm(diario, axis=1, keepdims=True)
unitarias = diario / normas
sim = unitarias @ unitarias.T          # 140 x 140
print("matriz de semelhança:", sim.shape)

usinas = [("Corumbá de Goiás", 0, 64),
          ("Cocalzinho", 64, 110),
          ("Abadiânia", 110, 140)]
for nome, a, b in usinas:
    bloco = sim[a:b, a:b]
    media = (bloco.sum(axis=1) - 1) / (b - a - 1)
    k = int(media.argmin())
    parado = int((diario[a + k] < 1).sum())
    print(f"{nome:17} inversor {a + k:3}: {media[k]:.4f} "
          f"(mediana {np.median(media):.4f}), "
          f"{parado} dias parado")
