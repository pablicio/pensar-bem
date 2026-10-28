from pathlib import Path

import skops.io as sio

from risco.campeao import treinado

VERSAO = "1.0.0"
destino = Path("modelos") / f"campeao-{VERSAO}.skops"
destino.parent.mkdir(exist_ok=True)
sio.dump(treinado(), destino)
print(f"gravado: {destino}")
