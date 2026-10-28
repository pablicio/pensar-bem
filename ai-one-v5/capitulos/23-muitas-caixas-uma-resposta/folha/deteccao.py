"""Detecção por janelas: alvos, rede, decodificar, NMS, AP."""
import torch
from torch import nn
from torch.utils.data import Dataset

from folha.caixas import do_conjunto, iou
from folha.conjunto import Folhas

JANELA, PASSO, LADO = 38, 8, 28     # 28 × 28 janelas
CENTROS = torch.arange(LADO) * PASSO + JANELA / 2


def codifica(caixa, cx, cy):
    """Uma caixa (cantos) como deslocamentos da janela."""
    centro = (caixa[:2] + caixa[2:]) / 2
    tamanho = caixa[2:] - caixa[:2]
    janela = torch.stack([cx, cy])
    return torch.cat([(centro - janela) / JANELA,
                      torch.log(tamanho / JANELA)])


class Janelas(Dataset):
    """Fotos de 256 e, para cada janela, se há lesão com centro
    a menos de um passo do centro dela, e os deslocamentos."""

    def __init__(self, qual):
        self.fotos = Folhas(qual, lado=256)
        todas = do_conjunto()
        self.caixas, self.alvos, self.desloc = [], [], []
        for linha in self.fotos.linhas:
            c = todas.get(linha["foto"], torch.zeros(0, 4))
            alvo = torch.zeros(LADO, LADO)
            desloc = torch.zeros(4, LADO, LADO)
            for caixa in c:
                cx, cy = (caixa[:2] + caixa[2:]) / 2
                perto_x = (cx - CENTROS).abs() < PASSO
                perto_y = (cy - CENTROS).abs() < PASSO
                for i in perto_y.nonzero().flatten():
                    for j in perto_x.nonzero().flatten():
                        alvo[i, j] = 1
                        desloc[:, i, j] = codifica(
                            caixa, CENTROS[j], CENTROS[i])
            self.caixas.append(c)
            self.alvos.append(alvo)
            self.desloc.append(desloc)

    def __len__(self):
        return len(self.fotos)

    def __getitem__(self, i):
        return self.fotos[i][0], self.alvos[i], self.desloc[i]


def rede_janelas():
    """Convoluções sem preenchimento: uma janela de 38 × 38
    vira 5 números; a foto de 256, um mapa de 28 × 28."""
    return nn.Sequential(
        nn.Conv2d(3, 16, 3), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(32, 64, 3), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(64, 64, 3), nn.ReLU(),
        nn.Conv2d(64, 5, 1))       # nota e 4 deslocamentos


def perda(saida, alvo, desloc):
    """Entropia cruzada binária em todas as janelas; L1 suave
    nos deslocamentos das janelas com lesão."""
    nota = nn.functional.binary_cross_entropy_with_logits(
        saida[:, 0], alvo)
    tem = alvo > 0
    if not tem.any():
        return nota
    previsto = saida[:, 1:].permute(0, 2, 3, 1)[tem]
    certo = desloc.permute(0, 2, 3, 1)[tem]
    return nota + nn.functional.smooth_l1_loss(previsto, certo)


def decodifica(saida, limiar=0.5):
    """Caixas (cantos, pixels de 256) e notas das janelas de um
    mapa 5 × 28 × 28 cuja probabilidade passa do limiar."""
    p = torch.sigmoid(saida[0])
    i, j = (p > limiar).nonzero(as_tuple=True)
    t = saida[1:, i, j]
    cx = CENTROS[j] + t[0] * JANELA
    cy = CENTROS[i] + t[1] * JANELA
    meia_l = JANELA * t[2].exp() / 2
    meia_a = JANELA * t[3].exp() / 2
    caixas = torch.stack([cx - meia_l, cy - meia_a,
                          cx + meia_l, cy + meia_a], dim=1)
    return caixas, p[i, j]


def nms(caixas, notas, limiar):
    """Supressão de não máximos: guarda a de maior nota e apaga
    as que a sobrepõem com IoU acima do limiar; repete."""
    ordem = notas.argsort(descending=True)
    guardadas = []
    while len(ordem):
        melhor = ordem[0]
        guardadas.append(melhor)
        sobre = iou(caixas[melhor][None], caixas[ordem[1:]])[0]
        ordem = ordem[1:][sobre <= limiar]
    return torch.stack(guardadas) if guardadas else ordem


def precisao_media(deteccoes, certas, limiar_iou=0.5):
    """AP de uma classe. deteccoes: por foto, (caixas, notas);
    certas: por foto, as caixas. Devolve a AP e as curvas de
    precisão e revocação."""
    acertos, notas = [], []
    for (caixas, nota), certo in zip(deteccoes, certas):
        usada = torch.zeros(len(certo), dtype=torch.bool)
        for k in nota.argsort(descending=True):
            acerto = False
            if len(certo):
                m = iou(caixas[k][None], certo)[0]
                m[usada] = 0           # cada certa uma vez
                melhor = m.argmax()
                if m[melhor] >= limiar_iou:
                    usada[melhor] = acerto = True
            acertos.append(acerto)
            notas.append(nota[k])
    ordem = torch.tensor(notas).argsort(descending=True)
    vp = torch.tensor(acertos)[ordem].float().cumsum(dim=0)
    total = sum(len(c) for c in certas)
    precisao = vp / torch.arange(1, len(vp) + 1)
    revocacao = vp / total
    envelope = precisao.flip(0).cummax(dim=0).values.flip(0)
    passo = torch.diff(revocacao, prepend=torch.zeros(1))
    return (passo * envelope).sum().item(), precisao, revocacao
