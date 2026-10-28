import numpy as np
import torch

from dados.gerar_malha import malha
from lauber.anomalia import (Malha, carrega_malha, escores,
                             mapa_de_erro)

FOTOS_ANO = 46 * 4 * 3600 * 24 * 365     # câmeras x segundos
DEVOLUCAO = 1_100_000                    # reais por ano
PARTE = {"furo": 0.5, "agulha": 0.3, "mancha": 0.2}
ALARME = 4.0           # reais: cinco minutos de um mecânico
EQUIPAMENTO = 46 * 3_500 + 15_000   # câmeras e um computador
rede = Malha()
rede.load_state_dict(torch.load("malha.pt"))


def escore(fotos):
    x = torch.tensor(np.array(fotos), dtype=torch.float32)
    return escores(mapa_de_erro(rede, x[:, None]))[1].numpy()


# cem mil fotos boas dos artigos conhecidos
sorteio = np.random.default_rng(9)
artigos = sorteio.choice(["preta", "branca", "azul"], 100_000)
boas = np.concatenate([
    escore([np.clip(malha(sorteio, a), 0, 1) for a in lote])
    for lote in np.array_split(artigos, 20)])
calibra, avalia = boas[:50_000], boas[50_000:]
_, teste, info = carrega_malha()
defeitos = escore(teste.numpy()[:, 0])
tipo = info["tipo_teste"]
print("limiar  falso/foto  pares/ano  furo agulha mancha"
      "  economia/ano")
for nome, limiar in (("99,9%", np.quantile(calibra, 0.999)),
                     ("99,99%", np.quantile(calibra, 0.9999)),
                     ("máximo", calibra.max())):
    um = (avalia > limiar).mean()
    # fotos boas independentes: um par de falsos tem chance um²
    pares = FOTOS_ANO * um ** 2
    achados = {}
    # o defeito aparece em 3 fotos seguidas: bastam 2
    for d in PARTE:
        p = (defeitos[tipo == d] > limiar).mean()
        nenhum_par = ((1 - p) ** 3 + 3 * p * (1 - p) ** 2
                      + p ** 2 * (1 - p))
        achados[d] = 1 - nenhum_par
    evitado = sum(DEVOLUCAO * PARTE[d] * achados[d]
                  for d in PARTE)
    economia = evitado - pares * ALARME
    texto = " ".join(f"{achados[d]:5.0%}" for d in PARTE)
    print(f"{nome:7} {um:10.5f} {pares:10,.0f} {texto}"
          f" {economia:13,.0f}")
print(f"equipamento: {EQUIPAMENTO:,} reais")
