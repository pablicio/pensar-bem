"""O desenho das estampas: seis famílias, à mão, por década.

Cada estampa é desenhada em 64 x 64 pixels e reduzida para 32,
o que suaviza as bordas. Todo motivo se repete num número
inteiro de vezes no quadro: a estampa emenda no rolo."""
import numpy as np

FAMILIAS = ["listra", "xadrez", "poa", "floral", "caxemira",
            "geometrico"]
# fundo e cores de motivo de cada década (RGB de 0 a 1)
PALETAS = {
    1960: [(.95, .91, .80), (.85, .65, .13), (.10, .50, .55),
           (.85, .40, .15), (.60, .15, .20)],
    1970: [(.93, .86, .70), (.55, .33, .15), (.85, .50, .10),
           (.45, .50, .20), (.75, .25, .10)],
    1980: [(.98, .98, .98), (.95, .20, .55), (.10, .70, .85),
           (.10, .10, .10), (.98, .85, .10)],
    1990: [(.92, .90, .85), (.10, .15, .40), (.50, .10, .15),
           (.15, .35, .20), (.70, .60, .40)],
    2000: [(.98, .95, .95), (.95, .70, .75), (.70, .85, .95),
           (.80, .90, .70), (.95, .85, .60)],
    2010: [(.97, .97, .95), (.95, .45, .40), (.55, .85, .75),
           (.20, .25, .35), (.95, .75, .30)],
    2020: [(.94, .90, .84), (.75, .40, .25), (.55, .65, .50),
           (.30, .25, .20), (.85, .70, .55)],
}


def grade(n=64):
    """Coordenadas de 0 a 1, sem repetir a borda."""
    t = np.arange(n) / n
    return np.meshgrid(t, t, indexing="ij")


def mancha_de_mao(sorteio, y, x, forca):
    """Um tremor suave e periódico: a mão de quem desenhou."""
    k = sorteio.integers(1, 3, size=2)
    fase = sorteio.uniform(0, 2 * np.pi, size=2)
    return forca * (np.sin(2 * np.pi * k[0] * x + fase[0])
                    + np.sin(2 * np.pi * k[1] * y + fase[1]))


def celula(y, x, n):
    """A posição dentro de cada célula, de -0,5 a 0,5."""
    return (y * n) % 1 - 0.5, (x * n) % 1 - 0.5


def listra(s, y, x, tremor):
    n = int(s.integers(3, 9))
    eixo = [y, x, (y + x) % 1][int(s.integers(3))]
    fase = (eixo * n + tremor) % 1
    return (fase < s.uniform(0.3, 0.6)).astype(float)


def xadrez(s, y, x, tremor):
    n = int(s.integers(2, 7))
    a = ((y * n + tremor) % 1) < 0.5
    b = ((x * n + tremor) % 1) < 0.5
    return 0.5 * a + 0.5 * b


def poa(s, y, x, tremor):
    n = int(s.integers(3, 7))
    dy, dx = celula(y, x, n)
    raio = s.uniform(0.18, 0.34)
    return (np.hypot(dy + tremor, dx) < raio).astype(float)


def floral(s, y, x, tremor):
    n = int(s.integers(2, 5))
    dy, dx = celula(y, x, n)
    petalas = int(s.integers(4, 7))
    r = np.hypot(dy, dx)
    ang = np.arctan2(dy, dx)
    # pétalas redondas: |cos| dá uma bossa por pétala
    borda = 0.16 + 0.22 * np.abs(np.cos(petalas * ang / 2))
    flor = (r < borda + tremor).astype(float)
    flor[r < 0.1] = 0.5                    # o miolo
    return flor


def caxemira(s, y, x, tremor):
    n = int(s.integers(2, 4))
    dy, dx = celula(y, x, n)
    giro = s.uniform(0, 2 * np.pi)
    r = np.hypot(dy, dx)
    # o ângulo torce com a distância: a ponta da gota se curva
    ang = np.arctan2(dy, dx) - giro + 3.0 * r
    gota = r < 0.13 + 0.25 * ((1 + np.cos(ang)) / 2) ** 4
    olho = np.hypot(dy, dx) < 0.06
    return (gota + tremor > 0.5) - 0.5 * olho


def geometrico(s, y, x, tremor):
    n = int(s.integers(2, 6))
    dy, dx = celula(y, x, n)
    if s.random() < 0.5:                   # losangos
        return (np.abs(dy) + np.abs(dx) < 0.35 + tremor) * 1.0
    zigue = np.abs(((x * n * 2) % 1) - 0.5)
    return (((y * n + zigue + tremor) % 1) < 0.4) * 1.0


DESENHOS = [listra, xadrez, poa, floral, caxemira, geometrico]


def desenha(sorteio, familia, decada, mao=0.02, tamanho=32):
    """Uma estampa (tamanho, tamanho, 3), de 0 a 1."""
    y, x = grade(2 * tamanho)
    tremor = mancha_de_mao(sorteio, y, x, mao)
    motivo = DESENHOS[familia](sorteio, y, x, tremor)
    paleta = np.array(PALETAS[decada])
    cores = sorteio.choice(len(paleta) - 1, size=2,
                           replace=False) + 1
    fundo = paleta[0]
    c1, c2 = paleta[cores[0]], paleta[cores[1]]
    um = np.clip(motivo, 0, 1)[..., None]
    meio = (np.abs(motivo - 0.5) < 0.25)[..., None]
    img = fundo * (1 - um) + c1 * um
    img = np.where(meio, c2, img)
    # de 64 para 32: média de cada bloco de 2 x 2
    img = img.reshape(tamanho, 2, tamanho, 2, 3)
    img = img.mean(axis=(1, 3))
    return img.astype(np.float32)
