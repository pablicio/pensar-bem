import numpy as np
import torch
import torch.nn.functional as F

from lauber.acervo import grade
from lauber.anomalia import Malha, carrega_malha, mapa_de_erro

treino, teste, info = carrega_malha()
rede = Malha()
rede.load_state_dict(torch.load("malha.pt"))
tipo = info["tipo_teste"]
verdade = torch.tensor(info["mascara_teste"])[:, None]
erro = F.avg_pool2d(mapa_de_erro(rede, teste), 3, stride=1,
                    padding=1)
# um limiar por pixel: o que só 0,1% dos pixels bons passam
bons = erro[torch.tensor(tipo == "bom")]
limiar = torch.quantile(bons.flatten()[::7], 0.999)
marcado = erro > limiar
# abertura: tira pontos soltos (erosão) e devolve o tamanho
# do que sobrou (dilatação)
erodido = -F.max_pool2d(-marcado.float(), 3, stride=1,
                        padding=1)
aberto = F.max_pool2d(erodido, 3, stride=1, padding=1) > 0
print(f"limiar por pixel: {limiar:.4f}")
print("tipo     achado  sobreposição  pixels marcados")
for d in ["bom", "furo", "agulha", "mancha"]:
    s = torch.tensor(tipo == d)
    achado = aberto[s].flatten(1).any(dim=1).float().mean()
    inter = (aberto[s] & verdade[s]).sum()
    uniao = (aberto[s] | verdade[s]).sum()
    iou = inter / uniao if d != "bom" else float("nan")
    marcados = aberto[s].float().mean()
    print(f"{d:8} {achado:6.0%} {iou:13.2f} {marcados:16.2%}")
# a agulha: a coluna com mais erro é a agulha quebrada
s = np.flatnonzero(tipo == "agulha")
coluna_prevista = erro[s].sum(dim=(1, 2)).argmax(dim=1)
coluna_certa = verdade[s].sum(dim=(1, 2)).argmax(dim=1)
acerto = (coluna_prevista - coluna_certa).abs() <= 1
taxa = acerto.float().mean()
print(f"agulha: coluna certa (±1) em {taxa:.0%}")
exemplos = [int(np.flatnonzero(tipo == d)[1])
            for d in ("furo", "agulha", "mancha")]
claro = (erro[exemplos] / erro.max()) ** 0.5   # realça o erro
linhas = [teste[exemplos], claro, aberto[exemplos].float(),
          verdade[exemplos].float()]
grade(torch.cat(linhas), "onde.png", colunas=3)
