"""A resposta inteira: três caixas, um número ou nada."""
import torch

from leitora.decide import TEMPERATURA
from leitora.recorte import caixa, como_mnist, em_branco


@torch.no_grad()
def le_resposta(modelo, folha, questao, t=TEMPERATURA):
    """O texto das três caixas, o número e a confiança."""
    texto, confianca = "", 1.0
    for k in range(3):
        tinta = caixa(folha, questao, k)
        if em_branco(tinta):
            texto += " "
            continue
        x = torch.from_numpy(como_mnist(tinta))[None]
        p = (modelo(x) / t).softmax(dim=1)[0]
        texto += str(int(p.argmax()))
        confianca *= p.max().item()
    numero = texto.lstrip()
    if numero == "":
        return texto, None, confianca         # em branco
    if " " in numero:
        return texto, "inválida", confianca   # buraco no meio
    return texto, int(numero), confianca
