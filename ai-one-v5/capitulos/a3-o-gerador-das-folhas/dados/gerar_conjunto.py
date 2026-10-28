"""As fotos de folhas da Folha Clara, de 2025 a 2027."""
import csv
from pathlib import Path

import numpy as np
from PIL import Image

from dados.camera import fotografa
from dados.desenho import desenha

SEMENTE = 2027
DESTINO = Path("dados/brutos")
FOLHAS = {"sadia": 560, "ferrugem": 460, "cercosporiose": 340,
          "bicho-mineiro": 120, "phoma": 240, "sol": 280}
MUNICIPIOS = ["Venda Nova do Imigrante", "Domingos Martins",
              "Brejetuba", "Afonso Cláudio", "Castelo", "Iúna",
              "Ibatiba", "Conceição do Castelo"]
FAZENDAS = 40
# com o que cada classe se confunde, para quem rotula
PARECIDA = {"sadia": "sol", "ferrugem": "sol",
            "sol": "ferrugem", "cercosporiose": "phoma",
            "phoma": "cercosporiose", "bicho-mineiro": "phoma"}


def rotula(s, verdade, intensidade, cuidado):
    """Um rótulo humano: erra mais quando há pouca doença."""
    erro = (0.02 + 0.12 * (intensidade < 0.6)) / cuidado
    return PARECIDA[verdade] if s.random() < erro else verdade


def gerar():
    s = np.random.default_rng(SEMENTE)
    for pasta in ("fotos", "mascaras", "lesoes"):
        (DESTINO / pasta).mkdir(parents=True, exist_ok=True)
    tons = s.uniform(0.94, 1.06, (FAZENDAS, 3))   # celulares
    municipio = s.integers(len(MUNICIPIOS), size=FAZENDAS)
    classes = [c for c, n in FOLHAS.items() for _ in range(n)]
    s.shuffle(classes)
    fotos, caixas, revisao = [], [], []
    n = 0
    for folha, verdade in enumerate(classes, 1):
        fazenda = int(s.integers(FAZENDAS))
        intensidade = s.uniform(0.4, 1.4)
        rotulo = rotula(s, verdade, intensidade, cuidado=1.0)
        p_lab = 0.8 if verdade == "ferrugem" else 0.08
        lab = s.random() < p_lab              # no laboratório
        semente = SEMENTE * 10_000 + folha
        desenho = desenha(semente, verdade, intensidade)
        for _ in range(1 + (s.random() < 0.5)):
            n += 1
            tipo = "mesa"
            if not lab:
                tipo = s.choice(["terra", "folhagem"])
            foto, mascara, ids, (ponta, peciolo) = fotografa(
                desenho, s, tipo,
                angulo=s.uniform(-15, 15),
                escala=s.uniform(0.85, 1.1),
                desloc=s.uniform(-10, 10, 2),
                luz=1.05 if lab else s.uniform(0.8, 1.15),
                tons=(1, 1, 1) if lab else tons[fazenda])
            nome = f"{n:06d}"
            Image.fromarray(foto).save(
                DESTINO / "fotos" / f"{nome}.jpg", quality=90)
            for pasta, arr in (("mascaras", mascara),
                               ("lesoes", ids)):
                Image.fromarray(arr).save(
                    DESTINO / pasta / f"{nome}.png")
            lugar = MUNICIPIOS[municipio[fazenda]]
            fotos.append([
                n, folha, f"F{fazenda + 1:02d}", lugar,
                verdade, rotulo, tipo, *np.round(ponta, 1),
                *np.round(peciolo, 1), int(ids.max())])
            for k in range(1, ids.max() + 1):
                ys, xs = np.nonzero(ids == k)
                if len(xs):
                    caixas.append([n, k, verdade, xs.min(),
                                   ys.min(), xs.max() + 1,
                                   ys.max() + 1])
    # 2027: o Dr. Edson revê 300 fotos; a Bia rotula as mesmas
    escolhidas = sorted(s.choice(n, 300, replace=False) + 1)
    por_foto = {f[0]: f for f in fotos}
    for k in escolhidas:
        verdade, rot = por_foto[k][4], por_foto[k][5]
        intens = 0.5 if rot != verdade else s.uniform(0.4, 1.4)
        revisao.append([k, rot,
                        rotula(s, verdade, intens, 1.2),
                        rotula(s, verdade, intens, 0.5)])
    escreve("fotos.csv",
            ["foto", "folha", "fazenda", "municipio",
             "verdade", "rotulo", "fundo", "ponta_x",
             "ponta_y", "peciolo_x", "peciolo_y", "lesoes"],
            fotos)
    escreve("caixas.csv", ["foto", "lesao", "tipo", "x0", "y0",
                           "x1", "y1"], caixas)
    escreve("revisao.csv",
            ["foto", "edson_2026", "edson_2027", "bia"],
            revisao)
    return n


def escreve(nome, cabecalho, linhas):
    caminho = DESTINO / nome
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cabecalho)
        w.writerows(linhas)


if __name__ == "__main__":
    print(f"{gerar()} fotos gravadas em {DESTINO}")
