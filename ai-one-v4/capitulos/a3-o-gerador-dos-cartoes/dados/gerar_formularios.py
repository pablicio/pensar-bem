"""Os cartões do verão de 2026, relidos pelas digitadoras."""
from pathlib import Path

import numpy as np

from dados.formulario import cartao, estilo

SEMENTE = 2026
PARTES = {"treino": 180, "validacao": 60, "teste": 60}
GABARITO = [42, 7, 315, 128, 9, 640, 77, 501, 18, 999]
VALENTINA = 31_877                  # a inscrição dela no verão


def respostas_de(sorteio):
    """O que um candidato escreveu: certo, errado ou nada."""
    r = []
    for certa in GABARITO:
        u = sorteio.random()
        if u < 0.06:
            r.append(None)          # deixou em branco
        elif u < 0.50:
            r.append(certa)
        else:
            r.append(int(sorteio.integers(0, 1000)))
    return r


def gerar():
    sorteio = np.random.default_rng(SEMENTE)
    inscricoes = sorteio.choice(np.arange(10_000, 50_000),
                                size=sum(PARTES.values()),
                                replace=False)
    fim = PARTES["treino"] + PARTES["validacao"] - 1
    inscricoes[fim] = VALENTINA      # o último da validação
    partes = np.repeat(list(PARTES), list(PARTES.values()))
    folhas, respostas, zeros = [], [], []
    for inscricao in inscricoes:
        e = estilo(sorteio)
        r = respostas_de(sorteio)
        if inscricao == VALENTINA:   # 7 cortado, 1 com serifa
            e.update(sete_cortado=True, um_serifa=True)
            r = [42, 7, 315, 128, 17, 640, 77, 501, 18, 711]
        folhas.append(cartao(r, e, sorteio))
        respostas.append([-1 if v is None else v for v in r])
        zeros.append(e["zeros_a_esquerda"])
    destino = Path("dados/brutos")
    destino.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(destino / "cartoes_verao.npz",
                        folhas=np.stack(folhas),
                        respostas=np.array(respostas),
                        zeros=np.array(zeros),
                        inscricoes=inscricoes,
                        partes=partes)
    return len(folhas)


if __name__ == "__main__":
    print(f"{gerar()} cartões gravados")
