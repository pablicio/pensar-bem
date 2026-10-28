import numpy as np
import torch
from PIL import Image

from folha.conjunto import PASTA, Folhas
from folha.olhar import gradcam
from folha.redes import rede_global
from folha.treino import lotes

valid = Folhas("validacao")
mascaras = []
for linha in valid.linhas:
    nome = f"{int(linha['foto']):06d}.png"
    m = Image.open(PASTA / "mascaras" / nome)
    m = m.resize((128, 128), Image.NEAREST)
    mascaras.append(np.array(m))
mascaras = torch.from_numpy(np.stack(mascaras))
folha, lesao = mascaras > 0, mascaras == 2
doente = lesao.flatten(1).any(dim=1)       # fotos com lesão
print(f"área média: folha {folha.float().mean():.0%},"
      f" lesão {lesao[doente].float().mean():.1%}")
print("rede          olhar na folha  na lesão")
for nome in ("sempre", "matiz", "matiz_fundos"):
    rede = rede_global()
    rede.load_state_dict(torch.load(f"{nome}.pt"))
    mapas = torch.cat([gradcam(rede, rede[10], x)
                       for x, _ in lotes(valid, 64)])
    total = mapas.sum(dim=(1, 2))
    na_folha = (mapas * folha).sum(dim=(1, 2)) / total
    na_lesao = (mapas * lesao).sum(dim=(1, 2)) / total
    print(f"{nome:13} {na_folha.mean():14.0%}"
          f" {na_lesao[doente].mean():9.0%}")
