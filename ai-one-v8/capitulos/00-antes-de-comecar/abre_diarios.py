from collections import Counter

from lupa.diario import atos, mostra

corpus = atos()
palavras = sum(len(a["texto"].split()) for a in corpus)
print(f"{len(corpus):,} atos, {palavras:,} palavras")
print("municípios:", len({a["municipio"] for a in corpus}))
print("de", corpus[0]["data"], "a", corpus[-1]["data"])
tipos = Counter(a["tipo"] for a in corpus)
for tipo, n in tipos.most_common():
    print(f"  {tipo:12} {n:6,}")
extrato = next(a for a in corpus if a["tipo"] == "extrato")
print("\n" + extrato["id"], extrato["municipio"],
      extrato["data"])
mostra(extrato["texto"])
