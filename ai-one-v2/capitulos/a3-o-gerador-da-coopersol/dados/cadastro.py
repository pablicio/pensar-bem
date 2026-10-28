"""O cadastro de cooperados, em planilha do Excel."""
import re
import zipfile
from datetime import date, datetime, timedelta

import numpy as np
from openpyxl import Workbook

from mundo import BRUTOS, COOPERADOS, RECADASTRO, USINAS, rng


NOMES = ["Maria", "José", "Ana", "João", "Antônio",
         "Francisca", "Carlos", "Luzia", "Paulo", "Conceição",
         "Pedro", "Sebastião", "Raimunda", "Lúcia", "Benedito",
         "Márcia", "Geraldo", "Aparecida", "Osvaldo", "Tereza",
         "Rogério", "Cláudia", "Edson", "Simone", "Valdir",
         "Débora", "Wanderley", "Iracema", "Divino", "Lázara"]
SOBRENOMES = ["Silva", "Souza", "Oliveira", "Pereira",
              "Lima", "Ferreira", "Costa", "Rodrigues",
              "Alves", "Gomes", "Ribeiro", "Martins", "Araújo",
              "Barbosa", "Rocha", "Mendonça", "Batista",
              "Conceição", "Magalhães", "Assunção", "Brandão",
              "Guimarães", "Simões", "Falcão", "Gonçalves"]
COMERCIOS = ["Padaria", "Pousada", "Oficina", "Mercearia",
             "Restaurante", "Farmácia", "Açougue",
             "Sorveteria"]
TIPOS = ["residencial", "comercio", "rural"]


def digitos_cpf(primeiro):
    # nove dígitos sorteados e os dois verificadores
    d = [primeiro] + [int(x) for x in rng.integers(0, 10, 8)]
    for n in (9, 10):
        soma = sum(v * (n + 1 - i) for i, v in enumerate(d))
        d.append(soma * 10 % 11 % 10)
    return "".join(str(v) for v in d)


def pontuado(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def montar_cadastro():
    pessoas = []
    for usina, n in COOPERADOS.items():
        for _ in range(n):
            tipo = rng.choice(TIPOS, p=[0.72, 0.18, 0.10])
            nome = (f"{rng.choice(NOMES)} "
                    f"{rng.choice(SOBRENOMES)} "
                    f"{rng.choice(SOBRENOMES)}")
            peso = {"residencial": rng.uniform(0.6, 1.4),
                    "comercio": rng.uniform(2.5, 6.0),
                    "rural": rng.uniform(1.8, 4.0)}[tipo]
            pessoas.append({"usina": usina, "tipo": str(tipo),
                            "nome": nome, "peso": peso})
    rng.shuffle(pessoas)
    usados = set()
    for p in pessoas:
        while True:
            cpf = digitos_cpf(int(rng.integers(0, 10)))
            if cpf not in usados:
                usados.add(cpf)
                p["cpf"] = cpf
                break
    # o Dirceu da padaria e o outro Dirceu, de Cocalzinho
    dirceu = next(p for p in pessoas
                  if p["usina"] == "abadiania"
                  and p["tipo"] == "comercio"
                  and p["cpf"][0] == "0")
    dirceu.update(nome="Dirceu Alves", peso=5.6,
                  comercio="Padaria Pão de Queijo da Matriz")
    outro = next(p for p in pessoas
                 if p["usina"] == "cocalzinho"
                 and p["tipo"] == "residencial")
    outro["nome"] = "Dirceu Alves"
    for p in pessoas:
        if p["tipo"] == "comercio" and "comercio" not in p:
            p["comercio"] = (f"{rng.choice(COMERCIOS)} "
                             f"{p['nome'].split()[1]}")
    # cotas em porcentagem com 4 casas, 100% por usina
    for usina in USINAS:
        grupo = [p for p in pessoas if p["usina"] == usina]
        pesos = np.array([p["peso"] for p in grupo])
        pct = np.round(pesos / pesos.sum() * 100, 4)
        pct[-1] = round(100 - pct[:-1].sum(), 4)
        for p, c in zip(grupo, pct):
            p["cota"] = float(c)
    # os 39 do recadastro: CPF começando com zero, em Abadiânia
    candidatos = [p for p in pessoas
                  if p["usina"] == "abadiania"
                  and p["cpf"][0] == "0" and p is not dirceu]
    escolhidos = [dirceu] + list(
        rng.choice(candidatos, RECADASTRO - 1, replace=False))
    for p in escolhidos:
        p["recadastro"] = True
    # ajuste fino: as cotas que fecham a história no centavo
    segunda = next(p for p in pessoas if p.get("recadastro")
                   and p is not dirceu)
    maior = max((p for p in pessoas
                 if p["usina"] == "abadiania"
                 and not p.get("recadastro")),
                key=lambda p: p["cota"])
    for p, nova in [(dirceu, 1.3954), (segunda, 0.1181)]:
        sobra = p["cota"] - nova
        maior["cota"] = round(maior["cota"] + sobra, 4)
        p["cota"] = nova
    return pessoas, dirceu


def gravar_cadastro(pessoas):
    wb = Workbook()
    ws = wb.active
    ws.title = "Cooperados"
    ws.append(["Código", "Nome", "CPF", "Tipo", "Usina",
               "Cota (%)", "Consumo médio (kWh)", "Situação",
               "Atualizado em"])
    usina_nome = {"corumba": "Corumbá de Goiás",
                  "cocalzinho": "Cocalzinho",
                  "abadiania": "Abadiânia"}
    novos = []
    for codigo, p in enumerate(pessoas, start=1001):
        jeito = rng.random()
        if jeito < 0.70:
            cpf = pontuado(p["cpf"])
        elif jeito < 0.85:
            cpf = p["cpf"]
        elif jeito < 0.95:
            cpf = f"{p['cpf'][:9]}-{p['cpf'][9:]}"
        else:
            cpf = f" {pontuado(p['cpf'])} "
        consumo = p["consumo"] if rng.random() > 0.04 else 0
        situacao = ("Inativo" if p.get("recadastro")
                    else "Ativo")
        ws.append([codigo, p["nome"], cpf, p["tipo"],
                   usina_nome[p["usina"]], p["cota"], consumo,
                   situacao, date(2023, 1, 1) + timedelta(
                       days=int(rng.integers(0, 1400)))])
        if p.get("recadastro"):
            novos.append(p)
    primeiro = 1001 + len(pessoas)
    for codigo, p in enumerate(novos, start=primeiro):
        ws.append([codigo, p["nome"], int(p["cpf"]), p["tipo"],
                   usina_nome[p["usina"]], p["cota"],
                   p["consumo"], "Ativo",
                   date(2027, 2, 1)
                   + timedelta(days=int(rng.integers(0, 6)))])
    wb.properties.creator = "Coopersol"
    wb.properties.created = datetime(2027, 3, 1, 8, 0)
    arquivo = BRUTOS / "cadastro_cooperados.xlsx"
    wb.save(arquivo)
    zip_fixo(arquivo)


def zip_fixo(arquivo):
    # regrava o .xlsx com datas fixas: mesmos bytes sempre
    with zipfile.ZipFile(arquivo) as z:
        partes = [(i.filename, z.read(i))
                  for i in z.infolist()]
    with zipfile.ZipFile(arquivo, "w",
                         zipfile.ZIP_DEFLATED) as z:
        for nome, dados in partes:
            if nome == "docProps/core.xml":  # hora da gravação
                dados = re.sub(rb"(modified[^>]*>)[^<]+",
                               rb"\g<1>2027-03-01T08:00:00Z",
                               dados)
            info = zipfile.ZipInfo(nome, (2027, 3, 1, 8, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, dados)
