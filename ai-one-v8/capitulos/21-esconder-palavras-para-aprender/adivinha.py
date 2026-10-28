import torch

from lupa.bert import BERT
from lupa.corpus import prepara
from lupa.diario import atos
from lupa.mlm import especiais

tok, treino, teste = prepara()
V = len(tok.vocab)
modelo = BERT(V)
modelo.load_state_dict(torch.load("bert.pt"))
modelo.eval()
MASK = especiais(V)["[MASK]"]
de_2027 = [a["texto"] for a in atos() if a["data"] >= "2027"]

# num ato de 2027, esconder uma palavra (com o espaço)
for palavra in [" uniformes", " meses", " Registre", " vigor"]:
    texto = next(t for t in de_2027 if palavra in t)
    esquerda, direita = texto.split(palavra, 1)
    antes = tok.codifica(esquerda)[-64:]
    depois = tok.codifica(direita)[:63]
    x = torch.tensor([antes + [MASK] + depois])
    with torch.no_grad():
        logits = modelo.saida(modelo(x))[0, len(antes)]
    melhores = logits.softmax(-1).topk(3)
    trecho = esquerda[-25:] + "[MASK]" + direita[:15]
    print(trecho.replace("\n", " "))
    print("  " + ", ".join(
        f"{tok.mostra(i)} {v:.2f}"
        for v, i in zip(melhores.values.tolist(),
                        melhores.indices.tolist())))
