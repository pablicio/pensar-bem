import time
import unicodedata

from lupa.diario import atos, mostra
from lupa.extrator import limpa
from lupa.tokenizador import PEDACO, Tokenizador

corpus = atos()
treino = [a["texto"] for a in corpus if a["data"] < "2027"]
teste = [a["texto"] for a in corpus if a["data"] >= "2027"]
amostra = teste[:200]

t = limpa(teste[0])
print("os pedaços cobrem o texto:",
      "".join(PEDACO.findall(t)) == t)
print(PEDACO.findall("CNPJ nº 67.422.200/0001-03")[:9])
todos = [p for t in treino for p in PEDACO.findall(limpa(t))]
print(len(todos), "pedaços,", len(set(todos)), "diferentes")

inicio = time.time()
tok = Tokenizador()
tok.treina(treino, 2000)
segundos = time.time() - inicio
print(f"{len(treino)} atos, V = 2000: {segundos:.0f} s")

volta = all(tok.decodifica(tok.codifica(t)) == limpa(t)
            for t in amostra)
print("decodifica(codifica(t)) == limpa(t):", volta)
n_bytes = sum(len(limpa(t).encode("utf-8")) for t in amostra)
n_tokens = sum(len(tok.codifica(t)) for t in amostra)
print(f"compressão: {n_bytes / n_tokens:.2f} bytes por token")

longos = sorted(tok.vocab, key=lambda i: -len(tok.vocab[i]))
print("os mais longos:")
mostra(" | ".join(tok.mostra(i) for i in longos[:4]))

frase = "Valor: R$ 13.948.112,40. Requalificação viária."
for forma in ["NFC", "NFD"]:
    ids = tok.codifica(unicodedata.normalize(forma, frase))
    print(forma, len(ids), "tokens")
mostra(" | ".join(tok.mostra(i) for i in ids))
print(tok.codifica("fim do ato<|fim|>"))
