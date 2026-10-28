import hashlib
from collections import Counter

from folha.conjunto import CLASSES, PASTA, parte, tabela


def resumo(dados):
    """Os 12 primeiros dígitos do SHA-256 de uns bytes."""
    return hashlib.sha256(dados).hexdigest()[:12]


linhas = tabela()
fotos = sorted((PASTA / "fotos").glob("*.jpg"))
todas = hashlib.sha256()
for f in fotos:                    # uma versão para as 2.980
    todas.update(f.read_bytes())
print(f"fotos/       {len(fotos)} arquivos, versão"
      f" {todas.hexdigest()[:12]}")
for nome in ("fotos.csv", "caixas.csv", "revisao.csv"):
    versao = resumo((PASTA / nome).read_bytes())
    print(f"{nome:12} versão {versao}")
partes = Counter(parte(f["fazenda"]) for f in linhas)
lista = ", ".join(f"{p} {n}" for p, n in partes.items())
print("\npartes:", lista)
total = Counter(f["rotulo"] for f in linhas)
mesa = Counter(f["rotulo"] for f in linhas
               if f["fundo"] == "mesa")
print("\nrótulo          fotos  na mesa azul")
for c in CLASSES:
    print(f"{c:14} {total[c]:6} {mesa[c]:13}")
