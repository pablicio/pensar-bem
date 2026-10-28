import matplotlib.pyplot as plt
import torch

from folha.deteccao import Janelas, decodifica, nms
from folha.deteccao import precisao_media, rede_janelas

valid = Janelas("validacao")
rede = rede_janelas()
rede.load_state_dict(torch.load("janelas.pt"))
rede.eval()
brutas, filtradas = [], []
with torch.no_grad():
    for i in range(len(valid)):
        caixas, notas = decodifica(rede(valid[i][0][None])[0],
                                   limiar=0.05)
        brutas.append((caixas, notas))
        k = nms(caixas, notas, 0.3)
        filtradas.append((caixas[k], notas[k]))
n_brutas = sum(len(c) for c, _ in brutas)
n_filtradas = sum(len(c) for c, _ in filtradas)
n_lesoes = sum(len(c) for c in valid.caixas)
print(f"{len(valid)} fotos, {n_lesoes} lesões; {n_brutas}"
      f" caixas antes do NMS, {n_filtradas} depois")
fig, ax = plt.subplots(figsize=(5, 3.4))
for nome, dets in (("sem NMS", brutas),
                   ("com NMS", filtradas)):
    for limiar in (0.3, 0.5, 0.7):
        ap, precisao, revocacao = precisao_media(
            dets, valid.caixas, limiar)
        print(f"{nome:8} AP a IoU {limiar}: {ap:.3f}")
        if limiar == 0.5:
            ax.plot(revocacao, precisao, label=nome)
ax.set_xlabel("revocação")
ax.set_ylabel("precisão")
ax.legend()
fig.tight_layout()
fig.savefig("pr.png", dpi=300)
