"""Os dados da leitora como Dataset do PyTorch."""
import numpy as np
import torch
from torch.utils.data import Dataset

from leitora.recorte import caixa, como_mnist, em_branco
from mnist import carregar


def digitos_da_resposta(resposta, zeros):
    """Os três rótulos; None é caixa em branco."""
    if resposta < 0:
        return [None, None, None]
    texto = f"{resposta:03d}" if zeros else f"{resposta:>3d}"
    return [None if c == " " else int(c) for c in texto]


class CaixasDoCartao(Dataset):
    """Cada caixa escrita dos cartões do verão, recortada."""

    def __init__(self, parte, transforma=None):
        d = np.load("dados/brutos/cartoes_verao.npz")
        escolhidos = np.where(d["partes"] == parte)[0]
        imagens, rotulos, origem = [], [], []
        for n in escolhidos:
            folha = d["folhas"][n]
            for q, resposta in enumerate(d["respostas"][n]):
                zeros = d["zeros"][n]
                rot = digitos_da_resposta(resposta, zeros)
                for k, r in enumerate(rot):
                    tinta = caixa(folha, q, k)
                    if r is None or em_branco(tinta):
                        continue
                    imagens.append(como_mnist(tinta))
                    rotulos.append(r)
                    origem.append((d["inscricoes"][n], q, k))
        self.imagens = torch.tensor(np.stack(imagens))
        self.rotulos = torch.tensor(rotulos)
        self.origem = origem
        self.transforma = transforma

    def __len__(self):
        return len(self.rotulos)

    def __getitem__(self, i):
        x = self.imagens[i]
        if self.transforma:
            x = self.transforma(x)
        return x, self.rotulos[i]


class MNIST(Dataset):
    """O MNIST do capítulo 0, como tensores de 0 a 1."""

    def __init__(self, parte):
        imagens, rotulos = carregar(parte)
        self.imagens = torch.tensor(imagens / 255,
                                    dtype=torch.float32)
        self.rotulos = torch.tensor(rotulos).long()

    def __len__(self):
        return len(self.rotulos)

    def __getitem__(self, i):
        return self.imagens[i], self.rotulos[i]
