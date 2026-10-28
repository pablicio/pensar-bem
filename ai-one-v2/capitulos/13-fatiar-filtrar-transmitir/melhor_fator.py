from datetime import date, timedelta

import numpy as np

diario = np.load("dados/processados/diario.npy")
potencia = np.array([2500 / 64] * 64 + [1800 / 46] * 46
                    + [1200 / 30] * 30)
fator = diario / (potencia[:, None] * 24) * 100
for nome, a, b in [("Corumbá de Goiás", 0, 64),
                   ("Cocalzinho", 64, 110),
                   ("Abadiânia", 110, 140)]:
    media = fator[a:b].mean(axis=0)
    i = int(media.argmax())
    quando = date(2026, 3, 1) + timedelta(days=i)
    print(f"{nome:17} {quando}  {media[i]:.1f}%")
