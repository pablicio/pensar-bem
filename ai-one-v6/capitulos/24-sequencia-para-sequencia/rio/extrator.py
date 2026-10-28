"""Da mensagem ao registro: um encoder-decoder."""
import re
from difflib import SequenceMatcher

import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence

from rio.leitor import preenche
from rio.texto import Vocabulario, caracteres, normaliza

CAMPOS = ["bairro", "rua", "numero", "pessoas"]
INICIO, FIM = "^", "$"


def registro(linha):
    """'vila nova|rua itoupava|412|2', sem acento."""
    return "|".join(normaliza(str(linha[c])) for c in CAMPOS)


def vocabularios(textos, registros):
    entrada = Vocabulario(textos, caracteres)
    saida = Vocabulario([INICIO + r + FIM for r in registros],
                        list, minimo=1)
    return entrada, saida


def alvos(saida, registros, maximo=62):
    marcados = [INICIO + r + FIM for r in registros]
    return preenche(saida, marcados, maximo)[0]


class Extrator(nn.Module):
    def __init__(self, n_entrada, n_saida, dim=32, estado=128):
        super().__init__()
        self.emb_e = nn.Embedding(n_entrada, dim,
                                  padding_idx=0)
        self.emb_s = nn.Embedding(n_saida, dim, padding_idx=0)
        self.encoder = nn.LSTM(dim, estado, batch_first=True)
        self.decoder = nn.LSTM(dim, estado, batch_first=True)
        self.saida = nn.Linear(estado, n_saida)

    def contexto(self, x, n):
        pacote = pack_padded_sequence(self.emb_e(x), n,
                                      batch_first=True,
                                      enforce_sorted=False)
        _, estado = self.encoder(pacote)
        return estado                    # (h, c) do fim

    def forward(self, x, n, y):
        """Teacher forcing: o decoder lê o registro certo e
        prevê, em cada posição, o caractere seguinte."""
        saidas, _ = self.decoder(self.emb_s(y[:, :-1]),
                                 self.contexto(x, n))
        return self.saida(saidas)

    @torch.no_grad()
    def extrai(self, x, n, saida, maximo=60):
        """Escreve o caractere mais provável, um por vez."""
        self.eval()
        estado = self.contexto(x, n)
        atual = torch.full((len(x), 1), saida.numero[INICIO])
        gerado = []
        for _ in range(maximo):
            s, estado = self.decoder(self.emb_s(atual), estado)
            atual = self.saida(s).argmax(2)
            gerado.append(atual)
        textos = []
        for seq in torch.cat(gerado, dim=1).tolist():
            texto = "".join(saida.tokens[i] for i in seq)
            textos.append(texto.split(FIM)[0])
        return textos


def treina_extrator(modelo, x, n, y, epocas=40, lote=64):
    otimo = torch.optim.Adam(modelo.parameters(), lr=2e-3)
    perda_fn = nn.CrossEntropyLoss(ignore_index=0)
    for epoca in range(epocas):
        modelo.train()
        for j in torch.randperm(len(x)).split(lote):
            z = modelo(x[j], n[j], y[j])
            perda = perda_fn(z.reshape(-1, z.shape[-1]),
                             y[j][:, 1:].reshape(-1))
            otimo.zero_grad()
            perda.backward()
            nn.utils.clip_grad_norm_(modelo.parameters(), 1.0)
            otimo.step()
        if (epoca + 1) % 10 == 0:
            valor = perda.item()
            print(f"época {epoca + 1}: perda {valor:.3f}")


EXTENSO = ["", "uma", "duas", "tres", "quatro", "cinco",
           "seis", "sete", "oito", "nove", "dez", "onze",
           "doze"]


def parecido(a, b):
    return SequenceMatcher(None, a, b).ratio()


def confere(gerado, texto):
    """Confere o registro com a mensagem: um número que não
    está nela vira o número dela mais parecido; um campo sem
    apoio no texto deixa o registro suspeito."""
    campos = gerado.split("|")
    if len(campos) != 4:
        return gerado, True
    limpo = normaliza(texto)
    numeros = re.findall(r"\d+", limpo)
    suspeito = any(c and c not in limpo for c in campos[:2])
    if campos[2] and campos[2] not in numeros:
        # com um número só na mensagem, não há o que confundir
        suspeito = suspeito or len(set(numeros)) != 1
        if numeros:
            alvo = campos[2]
            campos[2] = max(numeros,
                            key=lambda c: parecido(c, alvo))
    p = campos[3]
    if p and p not in numeros and not (
            p.isdigit() and int(p) < len(EXTENSO)
            and EXTENSO[int(p)] in limpo.split()):
        suspeito = True
    return "|".join(campos), suspeito
