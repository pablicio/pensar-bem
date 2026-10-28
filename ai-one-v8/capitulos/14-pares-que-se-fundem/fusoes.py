import time

from lupa.bpe import BPE
from lupa.diario import atos, mostra

corpus = atos()
treino = "\n".join(a["texto"] for a in corpus[:300])
novos = [a for a in corpus if a["data"] >= "2027"]
teste = [a["texto"] for a in novos[:200]]
print(len(treino.encode("utf-8")), "bytes de treino")

inicio = time.time()
bpe = BPE()
ids = bpe.treina(treino, 1000)
print(f"744 fusões em {time.time() - inicio:.0f} s")

print("\nas vinte primeiras fusões:")
for novo in range(256, 276):
    a, b = [p for p, n in bpe.fusoes.items() if n == novo][0]
    print(f"  {novo}: {bpe.mostra(a):>6} + {bpe.mostra(b):6}"
          f" -> {bpe.mostra(novo)}")

longo = max(bpe.vocab.values(), key=len)
print(f"\no mais longo, {len(longo)} bytes:")
mostra(longo.decode("utf-8"))

ok = all(bpe.decodifica(bpe.codifica(t)) == t for t in teste)
print("\ndecodifica(codifica(t)) == t no teste:", ok)
n_bytes = sum(len(t.encode("utf-8")) for t in teste)
n_tokens = sum(len(bpe.codifica(t)) for t in teste)
taxa = n_bytes / n_tokens
print(f"compressão no teste: {taxa:.2f} bytes por token")

for palavra in ["inexigibilidade", "requalificação"]:
    pedacos = [bpe.mostra(i) for i in bpe.codifica(palavra)]
    print(f"{palavra}: {' | '.join(pedacos)}")
