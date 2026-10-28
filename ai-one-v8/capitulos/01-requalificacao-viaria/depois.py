import re
import unicodedata
from collections import Counter

from lupa.diario import atos

PALAVRA = re.compile(r"\w+[-\w]*|[^\w\s]")
seguintes = {p: Counter() for p in
             ("pavimentação", "requalificação", "valor")}
for ato in atos():
    texto = unicodedata.normalize("NFC", ato["texto"])
    ps = PALAVRA.findall(texto.replace("-\n", ""))
    for a, b in zip(ps, ps[1:]):
        if a in seguintes:
            seguintes[a][b] += 1
for palavra, cont in seguintes.items():
    total = sum(cont.values())
    print(f"depois de '{palavra}' ({total} vezes):")
    for b, n in cont.most_common(3):
        print(f"  {b:12} {n / total:5.0%}")
