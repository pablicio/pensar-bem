"""Gera os diários oficiais do livro em dados/brutos.

    python -m dados.gerar_corpus

atos.jsonl          o corpus: um ano, de fev/2026 a jan/2027
producao.jsonl      os atos de fev a mai/2027, que o sistema lê
rotulos.jsonl       2.000 atos do corpus que a Patrícia rotulou
gabarito.jsonl      a verdade de todos (só o cap. 28 a abre)
empresas.csv        as empresas que existem, com CNPJ
palavras_chave.txt  a lista do Renan para a Cerrado Forte
"""
import csv
import hashlib
import json
import random
import unicodedata
from datetime import date, timedelta
from pathlib import Path

from .atos import TIPOS, monta, ruido
from .nomes import MUNICIPIOS, empresas, pessoa

SAIDA = Path(__file__).parent / "brutos"
TERMOS = """pavimentação pavimento pavimentar asfalto asfáltica
asfáltico asfaltamento recapeamento recape tapa-buraco
tapa-buracos CBUQ meio-fio meios-fios sarjeta sarjetas
drenagem bloquete bloquetes paralelepípedo terraplenagem
imprimação rodovia estrada vicinal ponte bueiro galeria
pluvial asfaltar asfaltada asfaltadas pavimentada
pavimentadas fresagem sub-base canaleta calçamento""".split()
EXPRESSOES = ["via pública", "vias públicas", "obra viária",
              "obras viárias", "pavimento rígido",
              "pavimento flexível", "capa asfáltica",
              "manta asfáltica", "massa asfáltica",
              "emulsão asfáltica", "concreto asfáltico",
              "piso intertravado", "lama asfáltica",
              "boca de lobo", "bocas de lobo", "rede pluvial",
              "tratamento superficial", "guia e sarjeta",
              "estrada vicinal", "meio fio", "tapa buraco"]


def sem_acento(t):
    t = unicodedata.normalize("NFD", t)
    return "".join(c for c in t
                   if unicodedata.category(c) != "Mn")


def palavras_chave():
    """Cada termo como o Renan escreveu: como é, sem acento,
    em maiúsculas e com inicial maiúscula."""
    lista = []
    for t in TERMOS + EXPRESSOES:
        s = sem_acento(t)
        for forma in (t, s, t.upper(), s.upper(), t.title()):
            if forma not in lista:
                lista.append(forma)
    return lista


def abre(nome):
    """Grava com fim de linha \\n também no Windows."""
    return open(SAIDA / nome, "w", encoding="utf-8",
                newline="\n")


def dias_uteis(inicio, fim):
    d = inicio
    while d <= fim:
        if d.weekday() < 5:
            yield d
        d += timedelta(days=1)


def agenda(rng, inicio, fim):
    """(data, município, tipo) de cada ato publicado."""
    pesos = [p for _, p in TIPOS.values()]
    for d in dias_uteis(inicio, fim):
        for mun, hab, _ in MUNICIPIOS:
            # cidade grande publica quase todo dia útil;
            # cidade pequena, duas vezes por semana
            if rng.random() > (0.9 if hab > 30_000 else 0.4):
                continue
            n = 1 + int(rng.random() * hab / 12_000)
            for tipo in rng.choices(list(TIPOS), pesos, k=n):
                yield d, mun, tipo, None


def main():
    rng = random.Random(2027)
    lista = empresas(rng)
    cadastro = {}
    for nome, cnpj, ramo in lista:
        cadastro.setdefault(ramo, []).append(
            (nome, cnpj, ramo))
    prefeitos = {m: pessoa(rng) for m, _, _ in MUNICIPIOS}
    pdf = {m: p for m, _, p in MUNICIPIOS}
    numero = {}
    gabarito = []
    SAIDA.mkdir(exist_ok=True)
    periodos = {"atos": (date(2026, 2, 2), date(2027, 1, 29)),
                "producao": (date(2027, 2, 1),
                             date(2027, 5, 28))}
    for nome, (ini, fim) in periodos.items():
        linhas = list(agenda(rng, ini, fim)) + especiais(nome)
        linhas.sort(key=lambda x: (x[0], x[1]))
        with abre(f"{nome}.jsonl") as f:
            for i, linha in enumerate(linhas):
                d, mun, tipo, especial = linha
                if especial:
                    texto, ent = especial(mun)
                    cat, raro = "viaria", True
                else:
                    chave = (mun, tipo, d.year)
                    numero[chave] = numero.get(chave, 0) + 1
                    c = {"mun": mun, "data": d,
                         "n": numero[chave],
                         "prefeito": prefeitos[mun],
                         "empresas": cadastro}
                    ato, cat, raro = TIPOS[tipo][0](rng, c)
                    texto, ent = monta(rng, ato, pdf[mun])
                ident = f"{nome[0]}{i:05d}"
                linha = {"id": ident, "municipio": mun,
                         "data": d.isoformat(), "tipo": tipo,
                         "texto": texto}
                f.write(json.dumps(linha, ensure_ascii=False)
                        + "\n")
                gabarito.append(
                    {"id": ident, "relevante": cat == "viaria",
                     "categoria": cat, "raro": raro,
                     "entidades": ent})
    rotulos(rng, gabarito)
    with abre("gabarito.jsonl") as f:
        for g in gabarito:
            f.write(json.dumps(g, ensure_ascii=False) + "\n")
    with abre("empresas.csv") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["nome", "cnpj", "ramo"])
        w.writerows(lista)
    with abre("palavras_chave.txt") as f:
        f.write("\n".join(palavras_chave()) + "\n")
    for arq in sorted(SAIDA.iterdir()):
        h = hashlib.sha256(arq.read_bytes()).hexdigest()[:16]
        print(f"{arq.name:20} {h}")


def rotulos(rng, gabarito):
    """2.000 atos do corpus, metade entre as contratações."""
    corpus = [g for g in gabarito if g["id"][0] == "a"]
    contrat = [g for g in corpus if g["categoria"]]
    outros = [g for g in corpus if not g["categoria"]]
    escolha = rng.sample(contrat, 1000) + rng.sample(outros,
                                                     1000)
    with abre("rotulos.jsonl") as f:
        for g in sorted(escolha, key=lambda g: g["id"]):
            linha = {"id": g["id"],
                     "relevante": g["relevante"],
                     "entidades": g["entidades"]}
            f.write(json.dumps(linha, ensure_ascii=False)
                    + "\n")


# ─── os dois atos da história ───────────────────────────────

MODELO = ("AVISO DE LICITAÇÃO\nCONCORRÊNCIA Nº {num}\n"
          "O Município de {mun}, por meio do Agente de"
          " Contratação, torna público que realizará"
          " licitação na modalidade concorrência, tipo menor"
          " preço global. Objeto: {objeto}. Valor estimado:"
          " {valor}. A sessão pública será realizada no dia"
          " {sessao}, às 9 horas. O edital está disponível na"
          " sede da Prefeitura.\n{mun}, {data}.\n"
          "{agente}\nAgente de Contratação")


def requalificacao(mun):
    """12/01/2027: a licitação que a Cerrado Forte não viu."""
    texto = MODELO.format(
        num="001/2027", mun=mun, sessao="27/01/2027",
        objeto="Obra de requalificação viária do eixo"
        " central, com regularização do leito, base e"
        " revestimento, calçadas acessíveis, ciclovia e"
        " sinalização, em extensão de 4,8 km",
        valor="R$ 13.948.112,40", data="12 de janeiro de 2027",
        agente="HELENA COSTA MARTINS")
    return texto, []


def readequacao(mun):
    """28/05/2027, sexta-feira: o diário do Seu Raimundo."""
    texto = MODELO.format(
        num="002/2027", mun=mun, sessao="11/06/2027",
        objeto="Obra de readequação de logradouros do Setor"
        " Central, com regularização do leito, base e"
        " revestimento das vias, em extensão de 2,1 km",
        valor="R$ 2.317.540,00", data="28 de maio de 2027",
        agente="RAIMUNDO NONATO BEZERRA")
    return ruido(random.Random(528), texto), []


ESPECIAIS = [
    ("atos", date(2027, 1, 12), "Nova Esperança do Cerrado",
     requalificacao),
    ("producao", date(2027, 5, 28),
     "Santo Antônio das Veredas", readequacao),
]


def especiais(nome):
    return [(d, mun, "aviso", fn)
            for n, d, mun, fn in ESPECIAIS if n == nome]


if __name__ == "__main__":
    main()
