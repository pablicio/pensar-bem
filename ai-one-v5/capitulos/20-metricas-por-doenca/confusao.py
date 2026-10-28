import torch
from sklearn.metrics import classification_report

from folha.conjunto import CLASSES
from folha.emprestada import treina_cabeca

matrizes = torch.load("caracteristicas.pt")
xt, yt = matrizes["treino"]
xv, yv = matrizes["validacao"]
prevista = treina_cabeca(xt, yt)(xv).argmax(dim=1)

M = torch.zeros(6, 6, dtype=torch.long)    # linha: certa
M.index_put_((yv, prevista), torch.ones_like(yv),
             accumulate=True)
cabecalho = " ".join(f"{c[:5]:>5}" for c in CLASSES)
print("certa \\ prevista " + cabecalho)
for c, linha in zip(CLASSES, M):
    print(f"{c:16} " + " ".join(f"{v:5}" for v in linha))

acertos = M.diagonal().float()
precisao = acertos / M.sum(dim=0)          # por coluna
revocacao = acertos / M.sum(dim=1)         # por linha
f1 = 2 * precisao * revocacao / (precisao + revocacao)
print("\nclasse          precisão  revocação     F1  fotos")
for i, c in enumerate(CLASSES):
    print(f"{c:15} {precisao[i]:9.3f} {revocacao[i]:10.3f}"
          f" {f1[i]:6.3f} {M[i].sum():6}")
print(f"{'macro':15} {precisao.mean():9.3f}"
      f" {revocacao.mean():10.3f} {f1.mean():6.3f}")
print(f"micro (= acerto): {acertos.sum() / M.sum():.3f}")
print()
print(classification_report(yv, prevista, target_names=CLASSES,
                            digits=3))
