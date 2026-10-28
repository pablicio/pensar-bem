"""Os arquivos dos três fabricantes de inversor."""
import json
from datetime import datetime, timedelta

import numpy as np

from ceu import PERFIL
from mundo import (API_V2, BRUTOS, DIAS, FIRMWARE, PASSOS, br,
                   dia, gravar, meses, rng)


def gravar_a(energia):
    pasta = BRUTOS / "inversores" / "corumba"
    pasta.mkdir(parents=True, exist_ok=True)
    n = energia.shape[2]
    nomes = [f"INV-{i + 1:02d}" for i in range(n)]
    for mes, ini, fim in meses():
        linhas = ["Usina Corumbá de Goiás;Fabricante A;"
                  "Exportação mensal",
                  "Data;Hora;Inversor;Energia"]
        for d in range(ini, fim):
            hoje = dia(d)
            em_kwh = FIRMWARE[0] <= hoje <= FIRMWARE[1]
            data = hoje.strftime("%d/%m/%Y")
            for p in range(PASSOS):
                hora = f"{p // 12:02d}:{p % 12 * 5:02d}"
                for i, nome in enumerate(nomes):
                    kwh = energia[d, p, i]
                    valor = (br(kwh, 4) if em_kwh
                             else br(kwh * 1000, 1))
                    linhas.append(
                        f"{data};{hora};{nome};{valor}")
        arquivo = pasta / f"corumba_{mes}.csv"
        gravar(arquivo, linhas, "latin-1")


def gravar_b(energia):
    pasta = BRUTOS / "inversores" / "cocalzinho"
    pasta.mkdir(parents=True, exist_ok=True)
    n = energia.shape[2]
    nomes = [f"B-{i + 1:02d}" for i in range(n)]
    for d in range(DIAS):
        hoje = dia(d)
        v2 = hoje >= API_V2
        meia_noite = datetime(hoje.year, hoje.month, hoje.day)
        leituras = []
        for p in range(PASSOS):
            inicio = meia_noite + timedelta(minutes=5 * p)
            if v2:
                utc = inicio + timedelta(hours=3)
                marca = utc.strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                marca = inicio.strftime("%Y-%m-%dT%H:%M:%S")
            for i, nome in enumerate(nomes):
                kwh = float(energia[d, p, i])
                if PERFIL[d, p] == 0:
                    kwh = -0.0008             # consumo noturno
                leituras.append({"inversor": nome,
                                 "inicio": marca,
                                 "energia_kwh": kwh})
        corpo = {"usina": "Cocalzinho",
                 "versao_api": "2" if v2 else "1",
                 "leituras": leituras}
        arquivo = pasta / f"{hoje.isoformat()}.json"
        arquivo.write_text(json.dumps(corpo), encoding="utf-8")


def gravar_c(energia):
    pasta = BRUTOS / "inversores" / "abadiania"
    pasta.mkdir(parents=True, exist_ok=True)
    n = energia.shape[2]
    nomes = [f"C-{i + 1:02d}" for i in range(n)]
    fora = set()                     # horas sem internet
    for d in rng.choice(np.arange(60, 200), 9, replace=False):
        inicio = int(rng.integers(60, 180))
        duracao = int(rng.integers(12, 48))
        for p in range(inicio, inicio + duracao):
            fora.add((int(d), p))
    for mes, ini, fim in meses():
        linhas = ["timestamp,inverter,energy_kwh"]
        for d in range(ini, fim):
            hoje = dia(d)
            for p in range(PASSOS):
                if (d, p) in fora:
                    continue
                hora = f"{p // 12:02d}:{p % 12 * 5:02d}:00"
                for i, nome in enumerate(nomes):
                    linhas.append(f"{hoje} {hora},{nome},"
                                  f"{energia[d, p, i]:.4f}")
        arquivo = pasta / f"abadiania_{mes}.csv"
        gravar(arquivo, linhas, "utf-8-sig")
    return fora
