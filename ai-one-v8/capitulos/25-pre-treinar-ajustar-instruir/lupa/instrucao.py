"""Pergunta e resposta sobre um ato, para o GPT pequeno."""
import re

import torch
import torch.nn.functional as F

from .extrator import limpa

PERGUNTAS = {"CONTRATADA": "Quem é a contratada?",
             "CNPJ": "Qual é o CNPJ da contratada?",
             "OBJETO": "Qual é o objeto?",
             "VALOR": "Qual é o valor?"}
CNPJ = re.compile(r"\d\d\.\d{3}\.\d{3}/\d{4}-\d\d")
VALOR = re.compile(r"R\$ [\d.]+,\d\d")


def respostas(texto, entidades):
    """As respostas certas, tiradas das anotações do ato."""
    r = {nome: limpa(texto[a:b]) for a, b, nome in entidades}
    r["VALOR"] = VALOR.match(r["VALOR"]).group()
    r["CNPJ"] = CNPJ.search(limpa(texto)).group()
    del r["PRAZO"]
    return r


def pergunta(tok, texto, chave, n=72):
    """O começo do ato (desde a contratada) e a pergunta."""
    limpo = limpa(texto)
    i = max(limpo.find("Contratada:"), 0)
    ids = tok.codifica(limpo[i:])[:n]
    return ids + tok.codifica(
        f"\nPergunta: {PERGUNTAS[chave]}\nResposta:")


def resposta(tok, texto):
    fim = tok.especial["<|fim|>"]
    return tok.codifica(" " + texto) + [fim]


def lote(pares, pad):
    """(pergunta, resposta) -> entrada, alvo; perda só na
    resposta, -100 na pergunta e no preenchimento."""
    T = max(len(p) + len(r) for p, r in pares)
    x = torch.full((len(pares), T), pad)
    y = torch.full((len(pares), T), -100)
    for k, (p, r) in enumerate(pares):
        s = p + r
        x[k, :len(s)] = torch.tensor(s)
        y[k, len(p) - 1:len(s) - 1] = torch.tensor(r)
    return x, y


def logp_resposta(modelo, pares, pad):
    """log P(resposta | pergunta), somado nos tokens."""
    x, y = lote(pares, pad)
    logp = F.log_softmax(modelo(x), -1)
    vale = y != -100
    tokens = logp.gather(-1, y.clamp(min=0)[..., None])[..., 0]
    return (tokens * vale).sum(1)


@torch.no_grad()
def responde(modelo, tok, ids, n=40):
    fim = tok.especial["<|fim|>"]
    x = torch.tensor([ids])
    for _ in range(n):
        prox = modelo(x[:, -modelo.T:])[0, -1].argmax().item()
        if prox == fim:
            break
        x = torch.cat([x, torch.tensor([[prox]])], dim=1)
    return tok.decodifica(x[0, len(ids):].tolist()).strip()
