import numpy as np
import torch
from scipy import ndimage

from folha.caixas import do_conjunto
from folha.treino import lotes
from folha.unet import Mascaras, UNet

valid = Mascaras("validacao")
rede = UNet()
rede.load_state_dict(torch.load("unet.pt"))
rede.eval()
with torch.no_grad():
    prevista = torch.cat([rede(x).argmax(dim=1)
                          for x, _ in lotes(valid, 32)])
reais, contadas = [], []
for p, m in zip(prevista.numpy(), valid.mascaras.numpy()):
    reais.append(ndimage.label(m == 2)[1])        # componentes
    contadas.append(ndimage.label(p == 2)[1])
reais, contadas = np.array(reais), np.array(contadas)
caixas = do_conjunto()
desenhadas = np.array([len(caixas.get(f["foto"], []))
                       for f in valid.fotos.linhas])
doentes = reais > 0
juntas = (desenhadas > reais)[doentes].mean()
media = desenhadas[doentes].mean()
print(f"lesões desenhadas por foto: {media:.1f};"
      f" fotos com lesões emendadas: {juntas:.0%}")
erro = np.abs(contadas - reais)[doentes]
print(f"fotos com lesão: {doentes.sum()};"
      f" manchas por foto: {reais[doentes].mean():.1f}")
print(f"erro médio da contagem: {erro.mean():.2f};"
      f" contagem exata em {(erro == 0).mean():.0%}")
print(f"fotos sadias com alguma mancha prevista:"
      f" {(contadas[~doentes] > 0).sum()}"
      f" de {(~doentes).sum()}")
