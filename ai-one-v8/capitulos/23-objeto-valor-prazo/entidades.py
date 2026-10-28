import torch
import torch.nn.functional as F

from lupa.bert import BERT
from lupa.corpus import prepara
from lupa.diario import atos, gabarito, le, mostra
from lupa.etiquetas import (ENTIDADES, ROTULOS, Etiquetador,
                            em_bytes, etiqueta, tensores,
                            tokens_e_posicoes, trechos_bio)

torch.set_num_threads(4)
tok, _, _ = prepara()
V = len(tok.vocab)
corpus = {a["id"]: a for a in atos()}
verdade = gabarito()


def exemplo(ident, entidades):
    texto = corpus[ident]["texto"]
    ids, posicoes = tokens_e_posicoes(tok, texto)
    trechos = [(*em_bytes(texto, a, b), nome)
               for a, b, nome in entidades]
    return ids, etiqueta(posicoes, trechos)


def de_2026(ident):
    return corpus[ident]["data"] < "2027"


treino = [exemplo(r["id"], r["entidades"])
          for r in le("rotulos.jsonl")
          if r["entidades"] and de_2026(r["id"])]
teste = [exemplo(i, g["entidades"]) for i, g in verdade.items()
         if g["entidades"] and i in corpus and not de_2026(i)]
print(f"treino {len(treino)} extratos, teste {len(teste)}")
ids, vazio, alvo = tensores(treino, V)
ids_t, vazio_t, alvo_t = tensores(teste, V)

# o fim de um valor escrito também por extenso
x, r = next((x, r) for x, r in treino
            if r.count("I-VALOR") > 20)
j = len(r) - 1 - r[::-1].index("I-VALOR")
trecho = zip(x[j - 4:j + 3], r[j - 4:j + 3])
mostra(" ".join(f"{tok.mostra(t)}/{e}" for t, e in trecho))


@torch.no_grad()
def avalia(modelo):
    """Por entidade: [acertos, previstos, reais]."""
    palpite = modelo(ids_t, vazio_t).argmax(-1)
    conta = {e: [0, 0, 0] for e in ENTIDADES}
    for k in range(len(teste)):
        vale = alvo_t[k] != -100
        real = trechos_bio([ROTULOS[i]
                            for i in alvo_t[k][vale]])
        prev = trechos_bio([ROTULOS[i]
                            for i in palpite[k][vale]])
        for grupo, coluna in [(real & prev, 0), (prev, 1),
                              (real, 2)]:
            for nome, *_ in grupo:
                conta[nome][coluna] += 1
    return conta


for nome, pre in [("BERT pré-treinado", True),
                  ("sem pré-treino", False)]:
    torch.manual_seed(0)
    bert = BERT(V)
    if pre:
        bert.load_state_dict(torch.load("bert.pt"))
    modelo = Etiquetador(bert)
    opt = torch.optim.AdamW(modelo.parameters(), lr=1e-3)
    for epoca in range(15):
        for k in range(0, len(ids), 32):
            logits = modelo(ids[k:k + 32], vazio[k:k + 32])
            perda = F.cross_entropy(logits.flatten(0, 1),
                                    alvo[k:k + 32].flatten())
            opt.zero_grad()
            perda.backward()
            opt.step()
    modelo.eval()
    if pre:
        torch.save(modelo.state_dict(), "etiquetas.pt")
    print(f"\n{nome}")
    soma = [0, 0, 0]
    for e, conta in avalia(modelo).items():
        vp, previstos, reais = conta
        f1 = 2 * vp / (previstos + reais)
        print(f"  {e:10}  F1 {f1:.3f}")
        soma = [s + n for s, n in zip(soma, conta)]
    vp, previstos, reais = soma
    f1 = 2 * vp / (previstos + reais)
    print(f"  {'todas':10}  F1 {f1:.3f}")
