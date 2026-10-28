import numpy as np
import torch
from PIL import Image
from torch.utils.data import TensorDataset

from dados.camera import fotografa
from dados.desenho import desenha
from dados.gerar_conjunto import FOLHAS
from folha.conjunto import CLASSES, Folhas
from folha.decisao import notas_fora_da_dobra, temperatura
from folha.emprestada import extrai, extratora, treina_cabeca
from folha.qualidade import confere, tensores
from folha.treino import fixar_semente

fixar_semente(0, nucleos=4)
s = np.random.default_rng(915)      # 15 de setembro
TIPOS = [c for c, n in FOLHAS.items() for _ in range(n)]
fotos, verdade, giro = [], [], []
for f in range(12):                 # 12 fazendas, 50 folhas
    for n in range(50):
        tipo = "aureolada" if s.random() < 0.02 else \
            str(s.choice(TIPOS))
        desenho = desenha(915_000 + 100 * f + n, tipo,
                          s.uniform(0.4, 1.4))
        giro.append(s.uniform(-180, 180))
        fundo = str(s.choice(["terra", "folhagem"]))
        foto, _, _, _ = fotografa(
            desenho, s, fundo, angulo=giro[-1],
            escala=s.uniform(0.85, 1.1),
            desloc=s.uniform(-10, 10, 2),
            luz=s.uniform(0.6, 1.2))
        img = Image.fromarray(foto)
        img = img.resize((128, 128), Image.BOX)
        fotos.append(np.array(img))
        verdade.append(tipo)

xt, yt = torch.load("caracteristicas.pt")["treino"]
T = temperatura(notas_fora_da_dobra(xt, yt), yt)
cabeca = treina_cabeca(xt, yt)
resnet = extratora()
dia = TensorDataset(tensores(fotos), torch.zeros(600).long())
f_dia, _ = extrai(resnet, dia)
f_val, _ = extrai(resnet, Folhas("validacao"))
unit = torch.nn.functional.normalize
treino_u = unit(xt, dim=1)
semelhanca = unit(f_dia, dim=1) @ treino_u.T
semelhanca = semelhanca.max(dim=1).values
normal = (unit(f_val, dim=1) @ treino_u.T).max(dim=1).values
limiar_sem = normal.quantile(0.01)      # como no capítulo 29
with torch.no_grad():
    p = (cabeca(f_dia) / T).softmax(dim=1)
conf, prevista = p.max(dim=1)
nome = [CLASSES[i] for i in prevista]
certo = torch.tensor([a == b for a, b in zip(nome, verdade)])
conhecida = torch.tensor([v != "aureolada" for v in verdade])
print(f"acerto da rede nas 600 folhas:"
      f" {certo.float().mean():.1%} (previsto: 86,8% a 90,1%)")
print(f"sem as {(~conhecida).sum()} aureoladas:"
      f" {certo[conhecida].float().mean():.1%}")

recusa = torch.tensor([confere(f) is not None for f in fotos])
estranha = (semelhanca < limiar_sem) & ~recusa
duvida = (conf < 0.93) & ~recusa & ~estranha
sozinho = ~recusa & ~estranha & ~duvida
print(f"\nrecusadas pelo filtro: {recusa.sum()};"
      f" estranhas: {estranha.sum()};"
      f" ao agrônomo: {duvida.sum()}")
print(f"decididas sozinhas: {sozinho.sum()}, acerto"
      f" {certo[sozinho].float().mean():.1%}")
aur = ~conhecida
print(f"aureoladas: {aur.sum()}; ao agrônomo ou estranhas:"
      f" {(aur & (duvida | estranha | recusa)).sum()};"
      f" decididas sozinhas: {(aur & sozinho).sum()}")

em_pe = torch.tensor([abs(g) <= 30 for g in giro])
for nome_g, grupo in (("folhas quase em pé", em_pe),
                      ("folhas tombadas", ~em_pe)):
    print(f"{nome_g:19} {grupo.sum():3}: decididas sozinhas"
          f" {sozinho[grupo].float().mean():.0%},"
          f" acerto da rede {certo[grupo].float().mean():.1%}")
