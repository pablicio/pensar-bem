import torch

from lupa.corpus import prepara
from lupa.diario import mostra
from lupa.gpt import GPT

tok, treino, teste = prepara()
modelo = GPT(len(tok.vocab))
modelo.load_state_dict(torch.load("gpt.pt"))
modelo.eval()
inicio = torch.tensor([[tok.especial["<|fim|>"]]])
gerador = torch.Generator().manual_seed(3)


def gulosa(logits):
    return logits.argmax(-1, keepdim=True)


def amostra(logits):
    p = torch.softmax(logits, -1)
    return torch.multinomial(p, 1, generator=gerador)


for nome, escolhe in [("gulosa", gulosa),
                      ("amostra", amostra)]:
    ids = modelo.gera(inicio, 400, escolhe)[0, 1:].tolist()
    atos = tok.decodifica(ids).split("<|fim|>")
    print(f"--- {nome}: o primeiro de {len(atos)} atos")
    mostra(atos[0])
    vezes = [sum(t in a for a in atos) for t in
             ("uniformes escolares", "R$ 10.533,00")]
    print("atos com uniformes escolares: {}, com"
          " R$ 10.533,00: {}".format(*vezes))
