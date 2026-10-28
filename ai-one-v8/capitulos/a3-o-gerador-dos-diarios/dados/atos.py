"""Os atos de um diário oficial, montados em pedaços.

Cada ato é uma lista de pedaços (texto, rótulo). O rótulo
marca as entidades de um extrato de contrato: OBJETO, VALOR,
PRAZO e CONTRATADA. Os diários feitos no editor de texto
passam por ruido(): acentos decompostos e palavras partidas
por hífen na quebra de linha.
"""
import unicodedata
from datetime import timedelta

from . import extenso
from .nomes import BAIRROS, contrai, feminino, pessoa
from .objetos import RAMO, objeto, valor_centavos

CARGOS = ["Secretário Municipal de Obras",
          "Secretária Municipal de Saúde",
          "Diretor de Departamento de Compras",
          "Assessor Jurídico", "Coordenadora Pedagógica",
          "Chefe de Gabinete", "Diretora de Cultura",
          "Secretário Municipal de Finanças"]
PREGAO = ["PREGÃO ELETRÔNICO", "PREGÃO PRESENCIAL"]
MODALIDADE = {"obra": ["CONCORRÊNCIA",
                       "CONCORRÊNCIA ELETRÔNICA"],
              "servico": PREGAO, "compra": PREGAO,
              "outro": ["PREGÃO ELETRÔNICO"]}
CLAUSULAS = [
    "Dotação orçamentária: 02.10.15.451.0021.1.015,"
    " elemento de despesa 4.4.90.51.",
    "Regime de execução: empreitada por preço unitário.",
    "Origem dos recursos: convênio nº {conv}/2026,"
    " celebrado com o Ministério das Cidades.",
    "Garantia contratual: 5% (cinco por cento) do valor do"
    " contrato.",
    "Fiscal do contrato: {fiscal}, CREA nº {crea}/D-GO.",
    "Fundamento legal: Lei Federal nº 14.133, de 1º de abril"
    " de 2021.",
    "Reajuste: anual, pelo Índice Nacional da Construção"
    " Civil.",
]


class Ato:
    def __init__(self):
        self.pedacos = []

    def __call__(self, texto, rotulo=None):
        self.pedacos.append((texto, rotulo))
        return self


def prefeito(c, maiusculas=False):
    """'o Prefeito' ou 'a Prefeita', conforme quem assina."""
    fem = feminino(c["prefeito"])
    p = "a Prefeita" if fem else "o Prefeito"
    return p.upper() if maiusculas else p


def assina(c):
    cargo = prefeito(c).split()[1]
    return f"{c['prefeito']}\n{cargo} Municipal"


def dias(n):
    return timedelta(days=n)


def maiusc(texto):
    return texto[0].upper() + texto[1:]


def prazo(rng, obra):
    n = rng.choice([3, 4, 6, 8, 10, 12, 18, 24] if obra
                   else [30, 60, 90, 120, 180, 12])
    unidade = "dias" if n >= 30 else "meses"
    return f"{n} ({extenso.numero(n)}) {unidade}"


def valor_texto(rng, centavos):
    texto = extenso.valor(centavos)
    if rng.random() < 0.4:
        texto += f" ({extenso.reais(centavos)})"
    return texto


def data_sessao(rng, d):
    sorteio = rng.random()
    if sorteio < 0.6:
        return d.strftime("%d/%m/%Y")
    if sorteio < 0.85:
        return extenso.data(d)
    return extenso.data_por_extenso(d)


def extrato(rng, c):
    texto, cat, raro = objeto(rng)
    obra = cat in ("viaria", "edificacao")
    emp, cnpj, _ = rng.choice(c["empresas"][RAMO[cat]])
    ano = c["data"].year
    a = Ato()
    a(f"EXTRATO DO CONTRATO Nº {c['n']:03d}/{ano}\n")
    a(f"Contratante: Município de {c['mun']}. Contratada: ")
    a(emp, "CONTRATADA")(f", CNPJ nº {cnpj}. Objeto: ")
    a(maiusc(texto), "OBJETO")(". Valor: ")
    a(valor_texto(rng, valor_centavos(rng, cat)), "VALOR")
    a(". Prazo: ")(prazo(rng, obra), "PRAZO")
    a(" a contar da assinatura.")
    # obras têm mais cláusulas: são os extratos longos
    k = rng.randint(3, 7) if obra else rng.randint(0, 2)
    for cl in rng.sample(CLAUSULAS, k):
        a(" " + cl.format(conv=rng.randrange(900_000, 999_999),
                          fiscal=pessoa(rng).title(),
                          crea=rng.randrange(10_000, 30_000)))
    assin = c["data"] - dias(rng.randint(1, 9))
    a(f" Data da assinatura: {extenso.data(assin)}.\n")
    a(assina(c))
    return a, cat, raro


def aviso(rng, c):
    texto, cat, raro = objeto(rng)
    modal = rng.choice(MODALIDADE[RAMO[cat]])
    sessao = c["data"] + dias(rng.randint(10, 30))
    hora = rng.choice([8, 9, 14])
    a = Ato()
    a(f"AVISO DE LICITAÇÃO\n{modal} Nº {c['n']:03d}/"
      f"{c['data'].year}\n")
    a(f"O Município de {c['mun']}, por meio do Agente de"
      " Contratação, torna público que realizará licitação"
      f" na modalidade {modal.lower()}, tipo menor preço"
      f" global. Objeto: {maiusc(texto)}.")
    if rng.random() < 0.7:
        cent = valor_centavos(rng, cat)
        a(f" Valor estimado: {valor_texto(rng, cent)}.")
    a(f" A sessão pública será realizada no dia"
      f" {data_sessao(rng, sessao)}, às {hora} horas."
      " O edital está disponível na sede da Prefeitura e no"
      " sítio eletrônico oficial do Município.\n")
    a(f"{c['mun']}, {extenso.data(c['data'])}.\n")
    a(f"{pessoa(rng)}\nAgente de Contratação")
    return a, cat, raro


def homologacao(rng, c):
    texto, cat, raro = objeto(rng)
    modal = rng.choice(MODALIDADE[RAMO[cat]])
    emp, cnpj, _ = rng.choice(c["empresas"][RAMO[cat]])
    cent = valor_centavos(rng, cat)
    a = Ato()
    a(f"TERMO DE HOMOLOGAÇÃO\n{modal} Nº {c['n']:03d}/"
      f"{c['data'].year}\n")
    a(f"{maiusc(prefeito(c))} Municipal de {c['mun']}"
      " HOMOLOGA o resultado do certame que tem por objeto:"
      f" {texto}, adjudicando-o à empresa {emp}, CNPJ nº"
      f" {cnpj}, pelo"
      f" valor global de {extenso.valor(cent)}.\n"
      "Publique-se.\n")
    a(f"{c['mun']}, {extenso.data(c['data'])}.\n")
    a(assina(c))
    return a, cat, raro


def aditivo(rng, c):
    texto, cat, raro = objeto(rng)
    emp, cnpj, _ = rng.choice(c["empresas"][RAMO[cat]])
    k = rng.choice([1, 1, 1, 2, 3])
    ano = c["data"].year - rng.choice([0, 1])
    a = Ato()
    a(f"EXTRATO DO {k}º TERMO ADITIVO AO CONTRATO Nº"
      f" {rng.randrange(1, 120):03d}/{ano}\n")
    a(f"Contratante: Município de {c['mun']}. Contratada:"
      f" {emp}, CNPJ nº {cnpj}. Objeto do contrato: {texto}. ")
    if rng.random() < 0.6:
        n = rng.choice([3, 6, 12])
        a("Objeto do aditivo: prorrogação do prazo de"
          f" vigência por mais {n} ({extenso.numero(n)})"
          " meses.")
    else:
        cent = valor_centavos(rng, cat) // 5
        pct = f"{rng.randrange(30, 250) / 10:.1f}"
        a(f"Objeto do aditivo: acréscimo de"
          f" {extenso.valor(cent)}, correspondente a"
          f" {pct.replace('.', ',')}% do valor inicial.")
    a(f"\n{c['mun']}, {extenso.data(c['data'])}.")
    return a, cat, raro


def contratacao_direta(rng, c):
    inex = rng.random() < 0.4
    texto, cat, raro = objeto(rng, "outro" if inex
                              else "compra")
    if inex:
        festa = rng.choice(["o carnaval municipal",
                            "a festa de aniversário do"
                            " município"])
        texto = f"contratação de show artístico para {festa}"
    emp, cnpj, _ = rng.choice(c["empresas"][RAMO[cat]])
    cent = valor_centavos(rng, cat) // (1 if inex else 8)
    nome = "INEXIGIBILIDADE" if inex else "DISPENSA"
    artigo = "74, inciso II" if inex else "75, inciso II"
    a = Ato()
    a(f"EXTRATO DE {nome} DE LICITAÇÃO Nº {c['n']:03d}/"
      f"{c['data'].year}\n")
    a(f"Objeto: {maiusc(texto)}. Contratada: {emp}, CNPJ nº"
      f" {cnpj}. Valor: {extenso.valor(cent)}. Fundamento:"
      f" art. {artigo}, da Lei nº 14.133/2021. Ratifico.\n")
    a(f"{c['mun']}, {extenso.data(c['data'])}.\n")
    a(assina(c))
    return a, cat, raro


def portaria(rng, c):
    verbo = rng.choice(["Nomear", "Nomear", "Exonerar"])
    liga = "para exercer o" if verbo == "Nomear" else "do"
    a = Ato()
    a(f"PORTARIA Nº {c['n']:03d}/{c['data'].year}\n")
    a(f"{prefeito(c, True)} MUNICIPAL DE"
      f" {c['mun'].upper()}, Estado de Goiás, no uso de suas"
      " atribuições legais, RESOLVE:\n")
    a(f"Art. 1º {verbo} {pessoa(rng)} {liga} cargo em"
      f" comissão de {rng.choice(CARGOS)}.\n")
    a("Art. 2º Esta Portaria entra em vigor na data de sua"
      " publicação.\nPublique-se. Registre-se. Cumpra-se.\n")
    quem = prefeito(c).replace("o P", "do P").replace(
        "a P", "da P")
    a(f"Gabinete {quem}, {extenso.data(c['data'])}.\n")
    a(assina(c))
    return a, None, False


def decreto(rng, c):
    mun = c["mun"].upper()
    chefe = prefeito(c, True)
    a = Ato()
    a(f"DECRETO Nº {c['n']:03d}, DE"
      f" {extenso.data(c['data']).upper()}\n")
    if rng.random() < 0.6:
        v = extenso.valor(rng.randrange(20_000, 3_000_000)
                          * 100)
        a(f"Abre crédito adicional suplementar no valor de {v}"
          " e dá outras providências.\n")
        a(f"{chefe} MUNICIPAL DE {mun} DECRETA:\n")
        a("Art. 1º Fica aberto crédito adicional suplementar"
          f" no valor de {v}, para reforço de dotações do"
          " orçamento vigente.\n")
    else:
        dia = c["data"] + dias(rng.randint(2, 12))
        dia = extenso.data(dia)
        a("Declara ponto facultativo nas repartições públicas"
          " municipais.\n")
        a(f"{chefe} MUNICIPAL DE {mun} DECRETA:\n")
        a(f"Art. 1º Fica declarado ponto facultativo no dia"
          f" {dia}.\n")
    a("Art. 2º Este Decreto entra em vigor na data de sua"
      " publicação.\nPublique-se. Cumpra-se.\n")
    a(assina(c))
    return a, None, False


def lei(rng, c):
    nome = pessoa(rng).title()
    bairro = contrai("em", rng.choice(BAIRROS))
    numero = f"{rng.randrange(1100, 2400):,}".replace(",", ".")
    a = Ato()
    a(f"LEI Nº {numero}, DE {extenso.data(c['data']).upper()}"
      "\n")
    a(f"Denomina via pública localizada {bairro}.\n")
    a(f"A CÂMARA MUNICIPAL DE {c['mun'].upper()} aprova e eu"
      " sanciono a seguinte Lei:\n")
    a(f"Art. 1º Fica denominada Rua {nome} o logradouro"
      f" público conhecido como Rua {rng.randrange(1, 40)}.\n")
    a("Art. 2º Esta Lei entra em vigor na data de sua"
      " publicação.\n")
    a(assina(c))
    return a, None, False


# tipo: (função, fração dos atos)
TIPOS = {"portaria": (portaria, 0.30),
         "extrato": (extrato, 0.18),
         "aviso": (aviso, 0.12),
         "decreto": (decreto, 0.10),
         "aditivo": (aditivo, 0.08),
         "homologacao": (homologacao, 0.08),
         "direta": (contratacao_direta, 0.08),
         "lei": (lei, 0.06)}


def hifeniza(rng, palavra):
    if (len(palavra) < 10 or "\n" in palavra
            or rng.random() > 0.15):
        return palavra
    corte = rng.randrange(4, len(palavra) - 3)
    if not palavra[corte].isascii():
        return palavra
    return palavra[:corte] + "-\n" + palavra[corte:]


def ruido(rng, texto):
    """O diário feito no editor de texto e salvo em PDF."""
    texto = unicodedata.normalize("NFD", texto)
    return " ".join(hifeniza(rng, p) for p in texto.split(" "))


def monta(rng, ato, pdf):
    """Junta os pedaços; devolve o texto e as entidades."""
    texto, entidades = "", []
    for pedaco, rotulo in ato.pedacos:
        if pdf:
            pedaco = ruido(rng, pedaco)
        if rotulo:
            fim = len(texto) + len(pedaco)
            entidades.append((len(texto), fim, rotulo))
        texto += pedaco
    return texto, entidades
