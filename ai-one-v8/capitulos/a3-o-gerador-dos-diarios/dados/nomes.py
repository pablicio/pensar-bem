"""Municípios, pessoas, empresas e ruas — todos inventados."""

# nome, habitantes, diário feito no editor de texto e
# exportado em PDF (acentos decompostos, hifenização)
MUNICIPIOS = [
    ("Jatobá dos Campos", 61_000, False),
    ("Lajeado do Buriti", 9_400, True),
    ("Santo Antônio das Veredas", 9_100, True),
    ("Nova Esperança do Cerrado", 88_000, False),
    ("Campo Alegre do Vão", 14_200, True),
    ("Pedra Branca de Goiás", 23_500, False),
    ("Buritizal do Leste", 7_800, True),
    ("Serra do Cocal", 31_000, False),
    ("Vereda Grande", 12_600, True),
    ("Ribeirão Seco", 44_000, False),
    ("Cachoeira do Jalapão", 5_900, True),
    ("Lagoa Formosa do Norte", 18_300, True),
    ("Morro do Pequi", 27_000, False),
    ("São Bento do Araguaia", 52_000, False),
    ("Taboca de Goiás", 6_700, True),
    ("Água Clara do Sul", 39_000, False),
    ("Capão Redondo do Cerrado", 11_200, True),
    ("Santa Luzia do Paranã", 76_000, False),
    ("Barreiro Fundo", 8_300, True),
    ("Palmital dos Goianos", 35_000, False),
    ("Córrego Fundo do Sul", 15_700, True),
    ("Itaberaba do Planalto", 120_000, False),
    ("Mangabeira de Goiás", 10_400, True),
    ("Rio Claro do Leste", 47_000, False),
    ("Poço Verde do Cerrado", 13_100, True),
    ("Alto Bonito", 22_000, False),
    ("Gameleira dos Campos", 6_200, True),
    ("Serra Dourada do Norte", 58_000, False),
    ("Baixa Funda", 9_900, True),
    ("Cristal do Planalto", 41_000, False),
    ("Olhos d'Água do Sul", 16_800, True),
    ("Santa Fé do Cerrado", 29_000, False),
    ("Vargem Bonita de Goiás", 7_100, True),
    ("Porto Seguro do Araguaia", 33_000, False),
    ("Boa Vista do Buriti", 12_000, True),
    ("Cajueiro do Vão", 19_500, True),
    ("Monte Alegre do Planalto", 66_000, False),
    ("Pirapora do Cerrado", 25_000, False),
    ("Taquari de Goiás", 8_800, True),
    ("Sítio Novo do Leste", 37_000, False),
]

NOMES = ("Ana Antônio Beatriz Carlos Cláudia Daniel Débora"
         " Eduardo Elaine Fábio Fernanda Gilberto Helena"
         " Igor Joana José Juliana Leonardo Lúcia Marcos"
         " Maria Mônica Otávio Paulo Raquel Ricardo Rosana"
         " Sérgio Simone Tiago Valéria Wagner").split()
SOBRENOMES = ("Almeida Barbosa Batista Cardoso Carvalho Costa"
              " Dias Ferreira Freitas Gomes Lima Machado"
              " Martins Mendes Moreira Nascimento Oliveira"
              " Pereira Pinto Ramos Ribeiro Rocha Santos"
              " Silva Soares Souza Teixeira Vieira").split()
BAIRROS = ("Centro|Setor Central|Vila Nova|Jardim América|"
           "Setor Aeroporto|Vila São José|Parque das Flores|"
           "Setor Sul|Jardim Primavera|Vila Operária|"
           "Setor Industrial|Residencial Buritis|Bairro Alto|"
           "Jardim Bela Vista|Setor Norte").split("|")
RUAS = ("Rua Goiás|Avenida Brasil|Rua 7 de Setembro|"
        "Avenida Tiradentes|Rua das Palmeiras|"
        "Avenida Bernardo Sayão|Rua Tocantins|"
        "Rua do Comércio|Avenida Goiânia|Rua São Paulo|"
        "Avenida Anhanguera|Rua dos Ipês|Rua Rui Barbosa|"
        "Avenida JK").split("|")


def contrai(prep, bairro):
    """'do Centro', 'da Vila Nova', 'no Setor Sul'..."""
    fem = bairro.startswith("Vila")
    art = {"de": ("da", "do"), "em": ("na", "no")}[prep]
    return f"{art[0] if fem else art[1]} {bairro}"


FEMININOS = set("Ana Beatriz Cláudia Débora Elaine"
                " Fernanda Helena Joana Juliana Lúcia Maria"
                " Mônica Raquel Rosana Simone Valéria".split())


def pessoa(rng):
    s1, s2 = rng.sample(SOBRENOMES, 2)
    return f"{rng.choice(NOMES)} {s1} {s2}".upper()


def feminino(nome):
    return nome.split()[0].title() in FEMININOS


def dv_cnpj(base12):
    """Os dois dígitos verificadores de um CNPJ."""
    digitos = [int(c) for c in base12]
    for pesos in ([5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2],
                  [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]):
        soma = sum(d * p for d, p in zip(digitos, pesos))
        resto = soma % 11
        digitos.append(0 if resto < 2 else 11 - resto)
    return digitos[-2:]


def formata_cnpj(base12):
    d = base12 + "".join(map(str, dv_cnpj(base12)))
    return f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:]}"


RAMOS = {
    "obra": ["CONSTRUTORA {} LTDA", "{} ENGENHARIA LTDA",
             "{} CONSTRUÇÕES E PAVIMENTAÇÃO LTDA",
             "{} INFRAESTRUTURA EIRELI",
             "{} OBRAS E SERVIÇOS LTDA"],
    "servico": ["{} SERVIÇOS URBANOS LTDA",
                "{} LIMPEZA E CONSERVAÇÃO EIRELI",
                "{} TRANSPORTES LTDA",
                "{} SOLUÇÕES AMBIENTAIS LTDA"],
    "compra": ["{} COMÉRCIO DE MEDICAMENTOS LTDA",
               "{} DISTRIBUIDORA DE ALIMENTOS LTDA",
               "{} COMBUSTÍVEIS LTDA",
               "{} PAPELARIA E INFORMÁTICA EIRELI",
               "{} COMÉRCIO E REPRESENTAÇÕES LTDA"],
    "outro": ["{} PRODUÇÕES ARTÍSTICAS LTDA",
              "{} CONSULTORIA E ASSESSORIA LTDA",
              "{} TECNOLOGIA EIRELI"],
}
PALAVRAS = ("ARAGUAIA BURITI CERRADO PLANALTO TOCANTINS IPÊ"
            " PEQUI VEREDA HORIZONTE PIONEIRA AURORA CENTRAL"
            " GOIANA ALIANÇA PROGRESSO FUTURA MODELO NOVA ERA"
            " SANTA CLARA BOA VISTA MONTE VERDE TRÊS IRMÃOS"
            " SÃO JORGE PRIMAVERA CAPITAL ESTRELA").split()


def empresas(rng, por_ramo=60):
    """O cadastro: nome, CNPJ com dígitos válidos e ramo."""
    vistas, lista = set(), []
    for ramo, modelos in RAMOS.items():
        while sum(e[2] == ramo for e in lista) < por_ramo:
            k = rng.choice([1, 2])
            nucleo = " ".join(rng.sample(PALAVRAS, k))
            nome = rng.choice(modelos).format(nucleo)
            if nome in vistas:
                continue
            vistas.add(nome)
            base = "".join(str(rng.randrange(10))
                           for _ in range(8))
            cnpj = formata_cnpj(base + "0001")
            lista.append((nome, cnpj, ramo))
    # o cliente da Lupa também aparece nos diários
    lista.append(("CONSTRUTORA CERRADO FORTE LTDA",
                  formata_cnpj("047182330001"), "obra"))
    return lista
