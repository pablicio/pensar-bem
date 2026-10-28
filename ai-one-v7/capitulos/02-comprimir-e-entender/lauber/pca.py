"""O PCA como compressão: projetar em k direções e voltar."""
import torch


class PCA:
    def __init__(self, imgs):
        """imgs: (N, C, H, W). Guarda a média e as direções."""
        x = imgs.flatten(1)                      # (N, D)
        self.forma = imgs.shape[1:]
        self.media = x.mean(dim=0)
        # X - média = U S V^T; as linhas de V^T são as direções
        _, s, vt = torch.linalg.svd(x - self.media,
                                    full_matrices=False)
        self.direcoes = vt                       # (D, D)
        self.variancia = s ** 2 / (len(x) - 1)

    def comprime(self, imgs, k):
        """Os k números de cada imagem: (N, k)."""
        x = imgs.flatten(1) - self.media
        return x @ self.direcoes[:k].T

    def descomprime(self, codigo):
        k = codigo.shape[1]
        x = codigo @ self.direcoes[:k] + self.media
        return x.view(-1, *self.forma)
