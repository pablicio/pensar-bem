import torch
from torch.utils.data import TensorDataset

from folha.emprestada import extrai, extratora
from folha.siamesa import Projecao, distancias, fotos_aureolada
from folha.treino import fixar_semente

fixar_semente(0, nucleos=4)
m = torch.load("caracteristicas.pt")
(xt, yt), (xv, yv) = m["treino"], m["validacao"]
x_aur = fotos_aureolada()
f_aur, _ = extrai(extratora(),
                  TensorDataset(x_aur, torch.zeros(60).long()))
projecao = Projecao()
projecao.load_state_dict(torch.load("projecao.pt"))
projecao.eval()
NOVA = 6                                  # a sétima classe


def unitaria(f):
    return torch.nn.functional.normalize(f, dim=1)


REPRESENTACOES = {"características da ResNet": unitaria,
                  "projeção da perda tripla": projecao}
teste = torch.cat([xv, f_aur[8:]])        # 449 conhecidas + 52
y_teste = torch.cat([yv, torch.full((52,), NOVA)])
print("representação              fotos  aureolada"
      "  conhecidas")
for nome, rep in REPRESENTACOES.items():
    with torch.no_grad():
        zt, z_teste = rep(xt), rep(teste)
        z_aur = rep(f_aur[:8])            # as 8 de suporte
    for k in (1, 5, 8):
        prototipos = torch.stack(
            [zt[yt == c].mean(dim=0) for c in range(6)]
            + [z_aur[:k].mean(dim=0)])    # média de k fotos
        d = distancias(z_teste, prototipos)
        prevista = d.argmin(dim=1)
        e_nova = y_teste == NOVA
        nova = (prevista[e_nova] == NOVA).float().mean()
        certas = prevista[~e_nova] == y_teste[~e_nova]
        velhas = certas.float().mean()
        print(f"{nome:27} {k:4} {nova:10.1%} {velhas:11.1%}")
