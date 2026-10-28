"""O Faster R-CNN da torchvision, ajustado às lesões."""
import torch
from torchvision.models.detection import (
    FasterRCNN_MobileNet_V3_Large_FPN_Weights,
    fasterrcnn_mobilenet_v3_large_fpn)
from torchvision.models.detection.faster_rcnn import (
    FastRCNNPredictor)

from folha.conjunto import Folhas
from folha.deteccao import precisao_media
from folha.yolo import TIPOS, caixas_com_tipo


def exemplos(qual):
    """(foto de 0 a 1, alvo) no formato da torchvision; o
    rótulo 0 é o fundo, e as doenças vão de 1 a 5."""
    fotos = Folhas(qual, lado=256)
    todas = caixas_com_tipo()
    lista = []
    for i, linha in enumerate(fotos.linhas):
        c = todas.get(linha["foto"], torch.zeros(0, 5))
        alvo = {"boxes": c[:, :4].clone(),
                "labels": c[:, 4].long() + 1}
        lista.append((fotos.imagens[i].float() / 255, alvo))
    return lista


def faster(lado):
    """Pesos do COCO; a foto é redimensionada para `lado`; a
    última camada passa a ter as 5 doenças e o fundo."""
    pesos = FasterRCNN_MobileNet_V3_Large_FPN_Weights.COCO_V1
    rede = fasterrcnn_mobilenet_v3_large_fpn(
        weights=pesos, min_size=lado, max_size=lado)
    cabeca = rede.roi_heads.box_predictor
    entrada = cabeca.cls_score.in_features
    rede.roi_heads.box_predictor = FastRCNNPredictor(
        entrada, len(TIPOS) + 1)
    rede.roi_heads.score_thresh = 0.01      # a AP quer a curva
    rede.roi_heads.detections_per_img = 200
    return rede


def ajusta(rede, dados, epocas, taxa=0.005, lote=4):
    """SGD com aquecimento nos 100 primeiros passos."""
    params = [p for p in rede.parameters() if p.requires_grad]
    otimizador = torch.optim.SGD(params, lr=taxa, momentum=0.9,
                                 weight_decay=1e-4)
    sorteador = torch.Generator().manual_seed(1)
    passo = 0
    for epoca in range(epocas):
        rede.train()
        ordem = torch.randperm(len(dados), generator=sorteador)
        total = 0.0
        for k in range(0, len(dados), lote):
            grupo = [dados[i] for i in ordem[k:k + lote]]
            # lote só de folhas sadias: perda indefinida
            if all(len(a["boxes"]) == 0 for _, a in grupo):
                continue
            for g in otimizador.param_groups:
                g["lr"] = taxa * min(1.0, (passo + 1) / 100)
            perdas = rede([x for x, _ in grupo],
                          [a for _, a in grupo])
            soma = sum(perdas.values())
            otimizador.zero_grad()
            soma.backward()
            otimizador.step()
            total += soma.item()
            passo += 1
        print(f"época {epoca + 1}: perda somada {total:.1f}")


@torch.no_grad()
def detecta(rede, x):
    """Caixas, notas e tipos (0 a 4) de uma foto."""
    rede.eval()
    saida = rede([x])[0]
    return saida["boxes"], saida["scores"], saida["labels"] - 1


def ap_por_tipo(deteccoes, certas, limiar_iou=0.5):
    """A AP de cada tipo. deteccoes: por foto, (caixas, notas,
    tipos); certas: por foto, tensor K × 5 (cantos e tipo)."""
    aps = []
    for t in range(len(TIPOS)):
        dets = [(c[k == t], n[k == t])
                for c, n, k in deteccoes]
        verdade = [c[c[:, 4] == t, :4] for c in certas]
        ap, _, _ = precisao_media(dets, verdade, limiar_iou)
        aps.append(ap)
    return aps
