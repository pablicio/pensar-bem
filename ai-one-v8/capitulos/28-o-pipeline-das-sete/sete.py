import time
from collections import defaultdict

import torch

from lupa.alerta import Lupa
from lupa.corpus import prepara
from lupa.diario import gabarito, le

torch.set_num_threads(4)
inicio = time.time()
tok, _, _ = prepara()
lupa = Lupa(tok)
preparo = time.time() - inicio
print(f"preparo (tokenizador e modelos): {preparo:.0f} s")
verdade = gabarito()

por_dia = defaultdict(list)
for a in le("producao.jsonl"):
    if a["data"] < "2027-05":             # fevereiro a abril
        por_dia[a["data"]].append(a)

alertas, tempos = [], []
for data in sorted(por_dia):
    inicio = time.time()
    alertas += lupa.dia(por_dia[data])
    tempos.append(time.time() - inicio)
n_atos = sum(len(v) for v in por_dia.values())
print(f"{len(por_dia)} dias, {n_atos} atos,"
      f" {len(alertas)} alertas")
print(f"por dia: média {sum(tempos) / len(tempos):.2f} s,"
      f" máximo {max(tempos):.2f} s")
for etapa, s in lupa.tempo.items():
    print(f"  {etapa}: {s:.1f} s no total")

relevantes = [a for v in por_dia.values() for a in v
              if verdade[a["id"]]["relevante"]]
certos = sum(verdade[a["id"]]["relevante"] for a in alertas)
print(f"alertas certos {certos}/{len(alertas)},"
      f" relevantes achados {certos}/{len(relevantes)}")

primeiro = next(a for a in alertas if "VALOR" in a)
print(f"\no primeiro alerta com valor, de {primeiro['data']}:")
for campo in ["municipio", "CONTRATADA", "OBJETO", "VALOR",
              "PRAZO"]:
    valor = primeiro.get(campo, "-")[:48]
    print(f"  {campo.lower():10} {valor}")
