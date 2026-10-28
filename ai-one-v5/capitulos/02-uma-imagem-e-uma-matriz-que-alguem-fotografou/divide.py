from collections import Counter

from folha.conjunto import CLASSES, parte, tabela

fotos = tabela()
partes = {"treino": [], "validacao": [], "teste": []}
for f in fotos:
    partes[parte(f["fazenda"])].append(f)

print(f"{'':10} {'fazendas':>8} {'folhas':>6} {'fotos':>5}  "
      + " ".join(f"{c[:5]:>5}" for c in CLASSES))
for nome, linhas in partes.items():
    fazendas = {f["fazenda"] for f in linhas}
    folhas = {f["folha"] for f in linhas}
    conta = Counter(f["rotulo"] for f in linhas)
    print(f"{nome:10} {len(fazendas):8} {len(folhas):6}"
          f" {len(linhas):5}  "
          + " ".join(f"{conta[c]:5}" for c in CLASSES))

# nenhuma folha e nenhuma fazenda em duas partes
for chave in ("folha", "fazenda"):
    grupos = [{f[chave] for f in p} for p in partes.values()]
    a, b, c = grupos
    comuns = (a & b) | (a & c) | (b & c)
    print(f"{chave}s em mais de uma parte: {len(comuns)}")
