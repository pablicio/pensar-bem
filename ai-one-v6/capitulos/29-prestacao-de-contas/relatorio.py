import numpy as np
import torch
from scipy.stats import beta

from rio.alerta import maximo_previsto
from rio.avalia import erro_nos_picos, mae, parte, picos
from rio.cota import julga
from rio.entradas import Escala, com_subidas, tabela
from rio.modelos import Previsor
from rio.provinha import PROVINHA
from rio.quantis import preve_quantis
from rio.texto import CLASSES, mensagens
from rio.treino import conjunto
from rio.triagem import carrega, triagem

FICHA = """## 1. O sistema

- Previsão: rede LSTM de quantis (5%, 50%, 95%), 72 h de
  entrada (níveis da cidade, Rio do Sul e Apiúna; quatro
  pluviômetros), 1 a 12 h à frente. Treino 1983–2002,
  validação 2003–2007, teste 2008–2026, com dados sintéticos.
- Alarme: quantil de 95% do maior nível em 12 h acima de
  5,5 m (limiar de Bayes de 2,5%); o fim do alarme só sai
  depois de 6 h abaixo da cota.
- Falhas: redes de reserva sem cada estação; sensor travado
  após 15 leituras iguais; sem previsão com as duas fora.
- Mensagens: média de uma LSTM e de um Naive Bayes; pilha de
  boatos acima de 0,5, revisada de hora em hora."""
LIMITES = """## 5. Limitações

- Seis cheias no teste: poucas para medir a taxa de aviso.
- Acima do maior nível do treino (9,05 m), a rede subestima
  a cheia (2008: {2008} m em 12 h); a regra de reserva chama o
  coordenador, mas não corrige o tamanho.
- Com Rio do Sul e Apiúna fora ao mesmo tempo, ou com o
  sensor da cidade fora, não há previsão.
- A triagem foi treinada com mensagens geradas por programa;
  em mensagens escritas por pessoas, acerta bem menos.
- O extrator inventa números de casa; todo registro é
  conferido com a mensagem e um terço vai para revisão.
- Os dados de treino são sintéticos; antes do uso, o sistema
  deve ser treinado de novo com a telemetria real."""


def br(valor, casas=1):
    return f"{valor:.{casas}f}".replace(".", ",")


H = tuple(range(1, 13))
tab = com_subidas(tabela())
nivel = tab["cidade"]
escalada = Escala(tab).aplica(tab)
x, y, horas = conjunto(escalada, nivel, "teste", H)
y = y.numpy() / 10
modelo = Previsor(x.shape[2], range(36), estado=64)
modelo.load_state_dict(torch.load("plantao.pt"))
q = preve_quantis(modelo, x)
r = ["# Sistema de alerta de Ribeirão das Pedras", "",
     FICHA, "", "## 2. Previsão do nível, teste 2008–2026", "",
     "| horizonte | erro médio | dentro da faixa | largura |",
     "|---|---|---|---|"]
for h in (1, 3, 6, 12):
    k = h - 1
    dentro = (y[:, k] >= q[:, k, 0]) & (y[:, k] <= q[:, k, 2])
    largura = (q[:, k, 2] - q[:, k, 0]).mean() * 100
    erro = mae(q[:, k, 1] - y[:, k]) * 100
    r.append(f"| {h} h | {br(erro)} cm | {dentro.mean():.0%}"
             f" | {largura:.0f} cm |")
r += ["", "## 3. As cheias do teste", "",
      "| pico | nível | previsto 12 h antes | aviso |",
      "|---|---|---|---|"]
teto = maximo_previsto(nivel.loc[horas].to_numpy(), q, 2)
cheias, antes, alarmes, falsos = julga(nivel, teto, horas)
erros = erro_nos_picos(nivel, q[:, 11, 1], horas, 12)
for pico, erro, ant in zip(picos(parte(nivel, "teste")),
                           erros, antes):
    real = nivel[pico]
    r.append(f"| {pico:%d/%m/%Y} | {br(real, 2)} m"
             f" | {br(real + erro, 2)} m | {ant:.0f} h |")
avisadas = len(antes)
piso = beta.ppf(0.05, avisadas, cheias - avisadas + 1)
r += ["",
      f"{avisadas} de {cheias} cheias avisadas (aviso contado"
      f" até 12 h);",
      f"{falsos} alarmes falsos em {alarmes}. Com {cheias}"
      " cheias, a taxa de",
      f"aviso pode ser de apenas {piso:.0%} (limite inferior"
      " de 95%)."]
voc, leitor, bayes = carrega()
msg = mensagens()
msg = msg[msg["data_hora"].dt.year >= 2023]
p = triagem(msg["texto"], voc, leitor, bayes).argmax(1)
verdade = msg["verdade"].map(CLASSES.index).to_numpy()
acerto = np.mean(p == verdade) * 100
risco = np.mean(p[verdade == 0] == 0) * 100
textos = [t for t, _ in PROVINHA]
pp = triagem(textos, voc, leitor, bayes).argmax(1)
yp = np.array([CLASSES.index(c) for _, c in PROVINHA])
riscos = np.sum((pp == 0) & (yp == 0))
r += ["", "## 4. Triagem das mensagens", "",
      f"- Teste 2023–2027: {br(acerto)}% de acerto; risco"
      f" reconhecido em {br(risco)}%.",
      f"- 24 mensagens escritas por pessoas:"
      f" {np.sum(pp == yp)} certas, {riscos} dos 6 riscos.",
      "", LIMITES.replace("{2008}", br(erros[0]))]
texto = "\n".join(r)
open("relatorio.md", "w", encoding="utf-8").write(texto + "\n")
print(texto)
