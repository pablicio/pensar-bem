"""Folhas de café e lesões, desenhadas em pé."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

L = 256                         # lado do desenho, em pixels
YY, XX = np.mgrid[0:L, 0:L].astype(float)


def ruido(s, escala):
    """Manchas suaves entre -0,5 e 0,5."""
    n = L // escala + 2
    peq = (s.random((n, n)) * 255).astype(np.uint8)
    img = Image.fromarray(peq).resize((L, L), Image.BICUBIC)
    return np.asarray(img, float) / 255 - 0.5


def suave(m, raio):
    """Desfoca uma máscara de 0 a 1."""
    m = (np.clip(m, 0, 1) * 255).astype(np.uint8)
    desfoque = ImageFilter.GaussianBlur(raio)
    img = Image.fromarray(m).filter(desfoque)
    return np.asarray(img, float) / 255


def pinta(img, alfa, cor):
    """Mistura a cor na imagem, na proporção alfa."""
    a = alfa[..., None]
    img[:] = img * (1 - a) + np.array(cor) / 255 * a


def folha(s):
    """Uma folha sadia: cor, opacidade, ponta e pecíolo."""
    comp = s.uniform(0.62, 0.74) * L            # comprimento
    larg = comp * s.uniform(0.42, 0.52)         # largura
    curva = s.uniform(-0.06, 0.06) * comp       # nervura torta
    t = np.linspace(0, 1, 160)                  # base → ponta
    meia = larg / 2 * np.sin(np.pi * t ** 0.9) ** 0.7
    onda = np.sin(t * s.uniform(25, 40) + s.uniform(0, 6))
    meia *= 1 + 0.025 * onda
    ponta = t > 0.8
    meia[ponta] *= np.linspace(1, 0.08, ponta.sum()) ** 1.3
    eixo = L / 2 + curva * np.sin(np.pi * t)
    y = L / 2 + comp / 2 - t * comp             # base embaixo
    esq = np.stack([eixo - meia * s.uniform(0.9, 1.0), y], 1)
    dir_ = np.stack([eixo + meia, y], 1)[::-1]
    contorno = Image.new("L", (L, L))
    ImageDraw.Draw(contorno).polygon(
        [tuple(p) for p in np.vstack([esq, dir_])], fill=255)
    alfa = suave(np.asarray(contorno, float) / 255, 0.8)

    # u atravessa a folha; v sobe da base (0) à ponta (1)
    v = (L / 2 + comp / 2 - YY) / comp
    u = XX - (L / 2 + curva * np.sin(np.pi * np.clip(v, 0, 1)))
    verde = np.array([38, 88, 36]) / 255
    cor = verde * s.uniform(0.85, 1.15) \
        + 0.05 * ruido(s, 12)[..., None] \
        + 0.02 * ruido(s, 3)[..., None]
    nervura = np.exp(-(u / 1.3) ** 2) * (v < 0.97)
    passo = s.uniform(0.06, 0.09) * comp
    fase = (v * comp - np.abs(u) * 0.8) % passo
    laterais = np.exp(-np.minimum(fase, passo - fase) ** 2) \
        * np.clip(1 - np.abs(u) / (larg * 0.45), 0, 1)
    cor = cor + 0.17 * nervura[..., None] \
        + 0.07 * laterais[..., None]
    lado = np.tanh(u / (larg * 0.25)) * s.choice([-1, 1])
    cor = cor * (1 + 0.12 * lado)[..., None]
    brilho = np.exp(-((u + larg * 0.15) ** 2
                      + ((v - 0.6) * comp) ** 2)
                    / (larg * comp * 0.15))
    cor = cor + 0.10 * brilho[..., None]

    # o pecíolo, um cabinho embaixo
    base = (eixo[0], y[0])
    fim = (eixo[0], y[0] + 16)
    talo = Image.new("L", (L, L))
    ImageDraw.Draw(talo).line([base, fim], fill=255, width=4)
    talo = np.asarray(talo, float) / 255
    pinta(cor, talo, (75, 105, 50))
    alfa = np.maximum(alfa, talo)
    ponta_xy = (eixo[-1], y[-1])
    return np.clip(cor, 0, 1), alfa, ponta_xy, fim


def mancha(s, centro, raio, torto):
    """Distância normalizada a uma mancha irregular."""
    ang = np.arctan2(YY - centro[1], XX - centro[0])
    f = s.uniform(0, 6, 3)
    r = raio * (1 + torto * (0.5 * np.sin(3 * ang + f[0])
                             + 0.3 * np.sin(5 * ang + f[1])
                             + 0.2 * np.sin(8 * ang + f[2])))
    return np.hypot(XX - centro[0], YY - centro[1]) / r


def lesao(cor, dentro, s, tipo, centro, tam=1.0):
    """Desenha uma lesão e devolve a máscara dela."""
    def disco(lim, raio):           # mancha suave, só na folha
        return suave((d < lim) * dentro, raio)

    if tipo == "ferrugem":          # pústulas alaranjadas
        d = mancha(s, centro, s.uniform(4, 9) * tam, 0.35)
        pinta(cor, disco(2.2, 3) * 0.5, (190, 190, 70))
        nucleo = (d < 1) & dentro
        pinta(cor, suave(nucleo, 0.8) * dentro, (220, 140, 30))
        po = (s.random((L, L)) < 0.55) & nucleo
        pinta(cor, po * 0.4, (240, 175, 60))
    elif tipo == "cercosporiose":   # olho pardo, centro claro
        d = mancha(s, centro, s.uniform(3.5, 7) * tam, 0.12)
        pinta(cor, disco(2.0, 2.5) * 0.55, (185, 180, 55))
        nucleo = (d < 1) & dentro
        pinta(cor, suave(nucleo, 0.6) * dentro, (115, 65, 35))
        pinta(cor, disco(0.55, 0.5), (205, 195, 175))
    elif tipo == "bicho-mineiro":   # mina clara, borda escura
        d = mancha(s, centro, s.uniform(9, 17) * tam, 0.6)
        nucleo = (d < 1) & dentro
        pinta(cor, suave(nucleo, 1.0) * dentro, (170, 135, 85))
        borda = suave(nucleo & (d > 0.8), 0.7)
        pinta(cor, borda * 0.7, (105, 75, 45))
        papel = (s.random((L, L)) < 0.3) & nucleo
        pinta(cor, papel * 0.25, (210, 190, 150))
    elif tipo == "phoma":           # necrose escura, na borda
        d = mancha(s, centro, s.uniform(12, 22) * tam, 0.5)
        nucleo = (d < 1) & dentro
        pinta(cor, disco(1.35, 2) * 0.6, (160, 150, 50))
        pinta(cor, suave(nucleo, 0.8) * dentro, (50, 32, 22))
    elif tipo == "sol":             # escaldadura, bronzeada
        d = mancha(s, centro, s.uniform(20, 32) * tam, 0.4)
        nucleo = (d < 1) & dentro
        rampa = np.clip(1.25 - d, 0, 1) * dentro
        pinta(cor, suave(rampa, 4) * 0.85, (185, 165, 95))
    elif tipo == "aureolada":       # a doença nova (cap. 31)
        d = mancha(s, centro, s.uniform(5, 9) * tam, 0.3)
        pinta(cor, disco(2.6, 2) * 0.7, (215, 205, 60))
        nucleo = (d < 1) & dentro
        pinta(cor, suave(nucleo, 0.7) * dentro, (80, 55, 30))
    return nucleo


QUANTAS = {"sadia": (0, 0), "ferrugem": (3, 12),
           "cercosporiose": (2, 9), "bicho-mineiro": (1, 4),
           "phoma": (1, 3), "sol": (1, 2), "aureolada": (2, 6)}


def desenha(semente, tipo, intensidade=1.0):
    """A folha da semente, com as lesões do tipo pedido."""
    s = np.random.default_rng(semente)
    cor, alfa, ponta, peciolo = folha(s)
    dentro = alfa > 0.5
    lugares = np.argwhere(dentro)
    if tipo == "phoma":             # perto da borda
        dist = np.hypot(*(lugares - lugares.mean(0)).T)
        lugares = lugares[dist > np.quantile(dist, 0.85)]
    poeira = s.random() < 0.3       # sujeira não é doença
    for _ in range(s.integers(1, 6) if poeira else 0):
        y, x = lugares[s.integers(len(lugares))]
        d = mancha(s, (x, y), s.uniform(1.5, 3), 0.2)
        sujo = suave((d < 1) & dentro, 0.6)
        pinta(cor, sujo * 0.5, (120, 110, 90))
    lo, hi = QUANTAS[tipo]
    n = 0
    if hi:
        sorteio = s.integers(lo, hi + 1)
        n = max(lo, round(sorteio * intensidade))
    tam = 0.6 + 0.4 * min(intensidade, 1.5)
    lesoes = []
    for _ in range(n):
        y, x = lugares[s.integers(len(lugares))]
        m = lesao(cor, dentro, s, tipo, (x, y), tam)
        if m.any():
            lesoes.append(m)
    return {"cor": cor, "alfa": alfa, "lesoes": lesoes,
            "ponta": ponta, "peciolo": peciolo}
