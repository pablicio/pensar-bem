import json
from datetime import date, timedelta
from pathlib import Path

import numpy as np

brutos = Path("dados/brutos/inversores")
inicio = date(2026, 3, 1)
dias = 365                 # março de 2026 a fevereiro de 2027
passos = 288               # intervalos de 5 minutos por dia
energia = np.full((140, dias, passos), np.nan)


def numero_br(texto):
    return float(texto.replace(".", "").replace(",", "."))


# fabricante A, inversores 0 a 63: o valor como está no arquivo
for caminho in sorted((brutos / "corumba").glob("*.csv")):
    with open(caminho, encoding="latin-1") as entrada:
        entrada.readline()
        entrada.readline()
        for linha in entrada:
            data, hora, inv, valor = linha.strip().split(";")
            d, m, a = data.split("/")
            dia = (date(int(a), int(m), int(d)) - inicio).days
            if not 0 <= dia < dias:
                continue
            passo = int(hora[:2]) * 12 + int(hora[3:]) // 5
            i = int(inv[4:]) - 1
            energia[i, dia, passo] = numero_br(valor)

# fabricante B, inversores 64 a 109: um JSON por dia
for dia in range(dias):
    hoje = inicio + timedelta(days=dia)
    caminho = brutos / "cocalzinho" / f"{hoje}.json"
    corpo = json.loads(caminho.read_text(encoding="utf-8"))
    valores = [l["energia_kwh"] for l in corpo["leituras"]]
    bloco = np.array(valores).reshape(passos, 46)
    energia[64:110, dia, :] = bloco.T

# fabricante C, inversores 110 a 139
for caminho in sorted((brutos / "abadiania").glob("*.csv")):
    with open(caminho, encoding="utf-8-sig") as entrada:
        entrada.readline()
        for linha in entrada:
            momento, inversor, valor = linha.strip().split(",")
            quando = date.fromisoformat(momento[:10])
            dia = (quando - inicio).days
            if not 0 <= dia < dias:
                continue
            passo = (int(momento[11:13]) * 12
                     + int(momento[14:16]) // 5)
            i = 110 + int(inversor[2:]) - 1
            energia[i, dia, passo] = float(valor)

destino = Path("dados/processados/leituras_ano.npy")
destino.parent.mkdir(parents=True, exist_ok=True)
np.save(destino, energia)
print(energia.shape, energia.dtype,
      f"{energia.nbytes / 1e6:.0f} MB")
print(int(np.isnan(energia).sum()), "leituras faltando")
