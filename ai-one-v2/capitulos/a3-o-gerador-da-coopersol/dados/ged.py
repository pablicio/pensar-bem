"""O rateio de cada mês e os arquivos da distribuidora."""
import numpy as np

from cadastro import pontuado
from ceu import CHUVA, NUVEM_DIA, PERFIL
from mundo import (API_V2, BRUTOS, DIAS, FIRMWARE, TARIFA, br,
                   dia, gravar, meses, rng)


def geracao(energia, presente, d0, d1, planilha=False):
    # kWh de cada usina entre os dias d0 e d1 (exclusive)
    a = energia["corumba"][d0:d1].sum()
    b = np.clip(energia["cocalzinho"][d0:d1], 0, None).sum()
    c = (energia["abadiania"][d0:d1]
         * presente[d0:d1, :, None]).sum()
    if planilha:
        for d in range(d0, d1):
            if FIRMWARE[0] <= dia(d) <= FIRMWARE[1]:
                a -= energia["corumba"][d].sum() * 0.999
            if dia(d) >= API_V2:     # 05h-19h lido em UTC
                tarde = energia["cocalzinho"][d, 16 * 12:]
                b -= np.clip(tarde, 0, None).sum()
    return {"corumba": round(float(a), 3),
            "cocalzinho": round(float(b), 3),
            "abadiania": round(float(c), 3)}


def creditos(pessoas, ger):
    # kWh e R$ de cada cooperado pela cota
    saida = {}
    for p in pessoas:
        kwh = round(ger[p["usina"]] * p["cota"] / 100, 2)
        saida[p["cpf"]] = (kwh, round(kwh * TARIFA, 2))
    return saida


def cpf_enviado(p):
    # o CPF que a planilha mandou: o do cadastro ativo
    if p.get("recadastro"):
        return str(int(p["cpf"]))      # o zero se perdeu
    return pontuado(p["cpf"])


def gravar_ged(pessoas, energia, presente):
    pasta = BRUTOS / "ged"
    (pasta / "compensacao").mkdir(parents=True, exist_ok=True)
    (BRUTOS / "envios").mkdir(parents=True, exist_ok=True)
    uc = {p["cpf"]: 3000000 + int(rng.integers(0, 999999))
          for p in pessoas}
    for mes, d0, d1 in meses():
        if mes == "2027-03":
            break                # março ainda não foi rateado
        real = geracao(energia, presente, d0, d1)
        usada = geracao(energia, presente, d0, d1,
                        planilha=True)
        enviado = creditos(pessoas, usada)
        linhas = ["CPF;Nome;kWh;Valor"]
        for p in pessoas:
            kwh, valor = enviado[p["cpf"]]
            linhas.append(f"{cpf_enviado(p)};{p['nome']};"
                          f"{br(kwh, 2)};{br(valor, 2)}")
        gravar(BRUTOS / "envios" / f"rateio_{mes}.csv", linhas,
               "utf-8")
        recadastro = mes >= "2027-02"
        sede = sum(real.values())
        linhas = ["Mês;UC;CPF;Nome;kWh compensado;Valor (R$)"]
        for p in pessoas:
            kwh, valor = enviado[p["cpf"]]
            if recadastro and p.get("recadastro"):
                kwh, valor = 0.0, 0.0  # CPF não encontrado
            sede -= kwh
            linhas.append(f"{mes};{uc[p['cpf']]};"
                          f"{pontuado(p['cpf'])};{p['nome']};"
                          f"{br(kwh, 2)};{br(valor, 2)}")
        sede = round(sede, 2)
        linhas.append(f"{mes};3000000;00.000.000/0001-00;"
                      f"SEDE COOPERSOL CERRADO;{br(sede, 2)};"
                      f"{br(round(sede * TARIFA, 2), 2)}")
        nome = f"compensacao_{mes}.csv"
        arquivo = pasta / "compensacao" / nome
        gravar(arquivo, linhas, "latin-1")


def gravar_consumo(pessoas):
    pasta = BRUTOS / "ged" / "consumo"
    pasta.mkdir(parents=True, exist_ok=True)
    medio = np.array([max(p["consumo"], 90) / 30
                      for p in pessoas])
    for mes, d0, d1 in meses():
        linhas = ["data,cpf,kwh"]
        for d in range(d0, d1):
            hoje = dia(d)
            fator = 0.9 if hoje.weekday() == 6 else 1.0
            calor = 1 + 0.12 * (1 - CHUVA[d])
            kwh = medio * fator * calor * rng.lognormal(
                0, 0.18, len(pessoas))
            for p, v in zip(pessoas, kwh):
                linhas.append(f"{hoje},{pontuado(p['cpf'])},"
                              f"{v:.2f}")
        if mes == "2027-02":         # um O no lugar de um zero
            campos = linhas[18402].split(",")
            campos[1] = "O" + campos[1][1:]
            linhas[18402] = ",".join(campos)
        gravar(pasta / f"consumo_{mes}.csv", linhas, "utf-8")


def gravar_estacao():
    linhas = ["data_hora,irradiancia_w_m2,"
              "temperatura_c,chuva_mm"]
    for d in range(DIAS):
        for h in range(24):
            sol = PERFIL[d, h * 12:(h + 1) * 12].mean()
            irr = (1050 * sol * NUVEM_DIA[d]
                   * rng.uniform(0.85, 1))
            temp = (19 + 9 * sol - 2 * CHUVA[d]
                    + rng.normal(0, 0.8))
            chuva = 0.0
            chance = 0.12 * CHUVA[d] * (1 - NUVEM_DIA[d])
            if rng.random() < chance:
                chuva = rng.exponential(4)
            linhas.append(f"{dia(d)} {h:02d}:00,{irr:.0f},"
                          f"{temp:.1f},{chuva:.1f}")
    gravar(BRUTOS / "estacao_corumba.csv", linhas, "utf-8")
