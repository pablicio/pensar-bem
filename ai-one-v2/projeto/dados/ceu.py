"""O céu de Goiás: sol, chuva e a energia de cada inversor."""
import numpy as np

from mundo import DIAS, PASSOS, dia, rng


def chuva_do_ano():
    # 1 no auge das chuvas (janeiro), 0 no auge da seca
    doy = np.array([dia(d).timetuple().tm_yday
                    for d in range(DIAS)])
    return 0.5 + 0.5 * np.cos(2 * np.pi * (doy - 15) / 365)


def perfil_solar():
    # fração da potência máxima em cada passo de cada dia
    doy = np.array([dia(d).timetuple().tm_yday
                    for d in range(DIAS)])[:, None]
    hora = (np.arange(PASSOS)[None, :] + 0.5) / 12
    duracao = 12 + 0.8 * np.cos(2 * np.pi * (doy - 355) / 365)
    nascer = 12.25 - duracao / 2
    x = np.clip((hora - nascer) / duracao, 0, 1)
    return np.sin(np.pi * x) ** 1.2


CHUVA = chuva_do_ano()
PERFIL = perfil_solar()
NUVEM_DIA = np.clip(
    0.97 - 0.55 * CHUVA * rng.beta(2, 2, DIAS), 0.15, 1)


def gerar_energia(mw, n):
    # kWh de cada inversor em cada passo: dias x passos x n
    clareza = np.clip(NUVEM_DIA + rng.normal(0, 0.04, DIAS),
                      0.1, 1)
    sombra = 1 - (rng.random((DIAS, PASSOS)) ** 4
                  * 0.7 * CHUVA[:, None])
    eficiencia = rng.normal(1, 0.015, n)
    kw = mw * 1000 / n * 0.82
    e = (PERFIL * clareza[:, None] * sombra)[:, :, None]
    e = e * eficiencia[None, None, :] * kw * 5 / 60
    parado = rng.random((DIAS, n)) < 0.003   # inversor parado
    e[np.broadcast_to(parado[:, None, :], e.shape)] = 0.0
    return np.round(e, 4)
