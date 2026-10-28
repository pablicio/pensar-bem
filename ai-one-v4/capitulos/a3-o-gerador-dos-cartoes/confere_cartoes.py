import hashlib

import numpy as np

cartoes = np.load("dados/brutos/cartoes_verao.npz")
for nome in cartoes.files:
    tabela = cartoes[nome]
    resumo = hashlib.sha256(tabela.tobytes()).hexdigest()
    print(resumo[:16], nome, tabela.shape)
