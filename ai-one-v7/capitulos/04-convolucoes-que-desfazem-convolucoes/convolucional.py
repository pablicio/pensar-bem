import time

import torch

from lauber.acervo import carrega, grade, partes
from lauber.autoencoder import Denso, erro, treina
from lauber.convolucional import Convolucional

imgs, _ = carrega()
treino, _, teste = partes(len(imgs))
amostra = imgs[teste[:6]]
cinza = torch.full((1, 3, 32, 32), 0.5)    # estampa lisa
redes = {"denso": Denso(codigo=256),
         "transposta": Convolucional("transposta"),
         "reamostra": Convolucional("reamostra")}
linhas, lisas = [amostra], []
print("rede        parâmetros   s  erro no teste  vizinhos")
for nome, rede in redes.items():
    torch.manual_seed(0)
    inicio = time.time()
    treina(rede, imgs[treino], epocas=10)
    segundos = time.time() - inicio
    with torch.no_grad():
        linhas.append(rede(amostra))
        lisa = rede(cinza)
    # numa estampa lisa, diferença entre vizinhos é defeito
    vizinhos = (lisa[..., 1:] - lisa[..., :-1]).abs().mean()
    total = sum(p.numel() for p in rede.parameters())
    print(f"{nome:10} {total:11,} {segundos:4.0f}"
          f" {erro(rede, imgs[teste]).mean():14.4f}"
          f" {vizinhos:9.4f}")
    # em cinza e com o contraste multiplicado por dez
    tom = lisa.mean(dim=1, keepdim=True)
    lisa = 0.5 + 10 * (tom - tom.mean())
    lisas.append(lisa.repeat(1, 3, 1, 1))
grade(torch.cat(linhas), "convolucionais.png", colunas=6)
grade(torch.cat(lisas), "tabuleiro.png", colunas=3,
      titulos=list(redes))
torch.save(redes["reamostra"].state_dict(), "convolucional.pt")
