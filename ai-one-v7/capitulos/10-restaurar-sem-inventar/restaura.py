import time

import numpy as np
import torch

from lauber.acervo import carrega, grade, partes
from lauber.autoencoder import treina
from lauber.convolucional import Convolucional
from lauber.restaura import Corretor, pares, psnr, ssim

escaneada, info = carrega("escaneada")
limpa, _ = carrega("limpa")      # só o gerador conhece
treino, _, teste = partes(len(escaneada))
# o treino: estampas que vieram sem dano, sujas de propósito
sem_dano = treino[info["dano"][treino] == ""]
entrada, alvo = pares(escaneada[sem_dano],
                      np.random.default_rng(3))
print(len(sem_dano), "pares de treino")
danificadas = teste[info["dano"][teste] != ""]
# as da Zuleica com erro proposital e algum dano
propositais = danificadas[info["proposital"][danificadas]]
redes = {"autoencoder": Convolucional(canais=16),
         "corretor": Corretor()}
print(f"{len(danificadas)} danificadas no teste,"
      f" {len(propositais)} delas com erro proposital")
print("             danificadas    erro proposital   treino")
print("             PSNR   SSIM      PSNR   SSIM")


def mede(nome, saida_d, saida_p, segundos=""):
    print(f"{nome:11}"
          f" {psnr(saida_d, limpa[danificadas]).mean():7.1f}"
          f" {ssim(saida_d, limpa[danificadas]).mean():6.3f}"
          f" {psnr(saida_p, limpa[propositais]).mean():11.1f}"
          f" {ssim(saida_p, limpa[propositais]).mean():6.3f}"
          f" {segundos:>8}")


mede("escaneada", escaneada[danificadas],
     escaneada[propositais])
linhas = [escaneada[propositais[:6]]]
for nome, rede in redes.items():
    torch.manual_seed(0)
    inicio = time.time()
    treina(rede, entrada, epocas=6, alvo=alvo)
    with torch.no_grad():
        mede(nome, rede(escaneada[danificadas]),
             rede(escaneada[propositais]),
             f"{time.time() - inicio:.0f} s")
        linhas.append(rede(escaneada[propositais[:6]]))
linhas.append(limpa[propositais[:6]])
grade(torch.cat(linhas), "restauracao.png", colunas=6)
