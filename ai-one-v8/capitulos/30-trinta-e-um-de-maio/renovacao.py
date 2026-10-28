import numpy as np
import torch

from lupa.ajuste import Classificador, tensores, treina
from lupa.alerta import Lupa
from lupa.bert import BERT
from lupa.corpus import prepara
from lupa.diario import atos, gabarito, le, mostra
from lupa.extrator import limpa

torch.set_num_threads(4)
tok, _, _ = prepara()
V = len(tok.vocab)
verdade = gabarito()
corpus = {a["id"]: a for a in atos()}
producao = le("producao.jsonl")
antigo = Lupa(tok).relevancia          # o que roda às sete


@torch.no_grad()
def probabilidade(modelo, lista):
    ids, vazio = tensores([a["texto"] for a in lista], tok)
    partes = [modelo(ids[i:i + 128], vazio[i:i + 128])
              .softmax(-1)[:, 1]
              for i in range(0, len(ids), 128)]
    return torch.cat(partes).numpy()


# os rótulos novos: os de 2026, agora com os raros, e o que a
# Patrícia leu de fevereiro a abril (os 35 suspeitos e os 100
# calmos sorteados do capítulo anterior, e os alertas)
fev_abr = [a for a in producao if a["data"] < "2027-05"]
p = probabilidade(antigo, fev_abr)
calmos = np.where(p < 0.001)[0]
sorteio = np.random.default_rng(0).choice(calmos, 100,
                                          replace=False)
lidos = [a for a, q in zip(fev_abr, p) if q >= 0.001]
lidos += [fev_abr[i] for i in sorteio]
rotulados = [corpus[r["id"]] for r in le("rotulos.jsonl")
             if corpus[r["id"]]["data"] < "2027"] + lidos
y = torch.tensor([int(verdade[a["id"]]["relevante"])
                  for a in rotulados])
print(f"rótulos novos: {len(rotulados)} atos,"
      f" {y.sum()} relevantes")

torch.manual_seed(0)
novo = Classificador(BERT(V))
novo.bert.load_state_dict(torch.load("bert.pt"))
ids, vazio = tensores([a["texto"] for a in rotulados], tok)
treina(novo, ids, vazio, y, novo.parameters(), lr=3e-4)
torch.save(novo.state_dict(), "relevancia_maio.pt")

maio = [a for a in producao if a["data"] >= "2027-05"]
real = np.array([verdade[a["id"]]["relevante"] for a in maio])
raro = np.array([verdade[a["id"]]["raro"] for a in maio])
k = next(i for i, a in enumerate(maio) if a["id"] == "p04221")
print(f"maio: {len(maio)} atos, {real.sum()} obras,"
      f" {raro.sum()} com palavras raras")
for nome, modelo in [("modelo das sete", antigo),
                     ("modelo novo", novo)]:
    q = probabilidade(modelo, maio)
    a = q > 0.5
    certos, raras = (a & real).sum(), (a & raro).sum()
    print(f"{nome}: {a.sum()} alertas, {certos} certos,"
          f" raras {raras}/{raro.sum()}")
    print(f"  Santo Antônio das Veredas, 28/5: p = {q[k]:.3f}")

print()
mostra(limpa(maio[k]["texto"]))
