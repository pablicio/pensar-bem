import hashlib

import numpy as np

for nome in ["acervo", "catalogo", "synapsys", "malha"]:
    dados = np.load(f"dados/brutos/{nome}.npz")
    soma = hashlib.sha256()
    for chave in sorted(dados.files):
        array = np.ascontiguousarray(dados[chave])
        soma.update(array.tobytes())
    tamanho = len(dados[dados.files[0]])
    resumo = soma.hexdigest()[:16]
    print(f"{resumo}  {nome + '.npz':14} {tamanho:6,}")
