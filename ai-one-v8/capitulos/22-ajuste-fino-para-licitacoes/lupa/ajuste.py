"""Ajustar o BERT a uma pergunta de sim ou não sobre o ato."""
import torch
import torch.nn.functional as F
from torch import nn

from .mlm import especiais


def tensores(textos, tok, T=128):
    """[CLS] + até T - 1 tokens, completados com [PAD]."""
    V = len(tok.vocab)
    CLS, PAD = especiais(V)["[CLS]"], especiais(V)["[PAD]"]
    ids = torch.full((len(textos), T), PAD)
    for i, t in enumerate(textos):
        x = [CLS] + tok.codifica(t)[:T - 1]
        ids[i, :len(x)] = torch.tensor(x)
    return ids, ids == PAD


class Classificador(nn.Module):
    """A média dos estados do BERT e uma camada linear."""

    def __init__(self, bert, d=128, classes=2):
        super().__init__()
        self.bert = bert
        self.cabeca = nn.Linear(d, classes)

    def forward(self, ids, vazio):
        h = self.bert(ids, vazio)                  # (B, T, d)
        cheio = (~vazio).unsqueeze(-1).float()
        media = (h * cheio).sum(1) / cheio.sum(1)  # (B, d)
        return self.cabeca(media)


def treina(modelo, ids, vazio, y, parametros, lr, epocas=4,
           B=32):
    opt = torch.optim.AdamW(parametros, lr=lr,
                            weight_decay=0.01)
    gerador = torch.Generator().manual_seed(0)
    modelo.train()
    for _ in range(epocas):
        ordem = torch.randperm(len(y), generator=gerador)
        for i in range(0, len(y), B):
            j = ordem[i:i + B]
            logits = modelo(ids[j], vazio[j])
            perda = F.cross_entropy(logits, y[j])
            opt.zero_grad()
            perda.backward()
            opt.step()
    modelo.eval()


@torch.no_grad()
def preve(modelo, ids, vazio, B=128):
    partes = [modelo(ids[i:i + B], vazio[i:i + B]).argmax(-1)
              for i in range(0, len(ids), B)]
    return torch.cat(partes)
