"""O objeto de cada contratação, por categoria.

Só a categoria "viaria" interessa à Construtora Cerrado
Forte. Uma em cada cinco obras viárias é escrita com palavras
que a lista de palavras-chave da Lupa não tem: as "raras".
"""
import math

from .nomes import BAIRROS, RUAS, contrai

VIARIA_COMUM = [
    "execução de obra de pavimentação asfáltica em CBUQ"
    " de vias urbanas {do_bairro}",
    "recapeamento asfáltico da {rua} e vias adjacentes",
    "serviços de tapa-buracos em vias públicas {do_bairro}",
    "construção de meio-fio, sarjeta e pavimentação da {rua}",
    "obra de drenagem pluvial e pavimentação asfáltica"
    " {no_bairro}",
    "pavimentação em bloquetes sextavados de ruas"
    " {do_bairro}",
    "execução de pavimentação asfáltica e drenagem de águas"
    " pluviais na {rua}",
    "restauração do pavimento asfáltico da {rua}",
]
VIARIA_RARA = [
    "requalificação viária da {rua}, com regularização do"
    " leito, base e revestimento",
    "revitalização do sistema viário {do_bairro}",
    "melhoria da trafegabilidade das vias {do_bairro}, com"
    " regularização do leito e revestimento",
    "readequação geométrica e implantação de binário na"
    " {rua}",
    "obra de infraestrutura urbana com abertura e"
    " revestimento de vias {no_bairro}",
]
EDIFICACAO = [
    "construção de escola municipal de ensino infantil"
    " {no_bairro}",
    "reforma e ampliação da Unidade Básica de Saúde"
    " {do_bairro}",
    "construção de quadra poliesportiva coberta {no_bairro}",
    "reforma do prédio da Câmara Municipal",
    "construção de creche {no_bairro}",
    "ampliação do cemitério municipal",
]
SERVICO = [
    "prestação de serviços de limpeza urbana, varrição e"
    " capina de vias públicas",
    "coleta e transporte de resíduos sólidos urbanos",
    "manutenção da iluminação pública do município",
    "transporte escolar de alunos da zona rural",
    "locação de máquinas pesadas para manutenção de"
    " estradas vicinais",
    "serviços de sinalização de trânsito e pintura de"
    " faixas",
]
COMPRA = [
    "aquisição de medicamentos para a rede municipal de"
    " saúde",
    "aquisição de gêneros alimentícios para a merenda"
    " escolar",
    "fornecimento de combustíveis para a frota municipal",
    "aquisição de material de expediente",
    "aquisição de massa asfáltica fria para a operação"
    " tapa-buracos",
    "aquisição de pneus para os veículos da frota municipal",
    "aquisição de uniformes escolares",
    "aquisição de cestas básicas para famílias em"
    " vulnerabilidade",
]
OUTRO = [
    "contratação de show artístico para a festa de"
    " aniversário do município",
    "assessoria e consultoria contábil",
    "licença de uso de sistema de gestão pública",
    "realização de concurso público",
]
MODELOS = {"edificacao": EDIFICACAO, "servico": SERVICO,
           "compra": COMPRA, "outro": OUTRO}
CATEGORIAS = {"viaria": 0.12, "edificacao": 0.10,
              "servico": 0.21, "compra": 0.39, "outro": 0.18}
RAMO = {"viaria": "obra", "edificacao": "obra",
        "servico": "servico", "compra": "compra",
        "outro": "outro"}
# faixa de valor de cada categoria, em reais
VALORES = {"viaria": (380_000, 9_000_000),
           "edificacao": (250_000, 4_000_000),
           "servico": (60_000, 2_500_000),
           "compra": (8_000, 900_000),
           "outro": (15_000, 300_000)}


def objeto(rng, categoria=None):
    """(texto, categoria, raro)"""
    if categoria is None:
        categoria = rng.choices(list(CATEGORIAS),
                                list(CATEGORIAS.values()))[0]
    raro = False
    if categoria == "viaria":
        raro = rng.random() < 0.2
        modelos = VIARIA_RARA if raro else VIARIA_COMUM
    else:
        modelos = MODELOS[categoria]
    b = rng.choice(BAIRROS)
    texto = rng.choice(modelos).format(
        do_bairro=contrai("de", b), no_bairro=contrai("em", b),
        rua=rng.choice(RUAS))
    if categoria == "viaria" and rng.random() < 0.6:
        km = f"{rng.randrange(8, 120) / 10:.1f}"
        texto += f", em extensão de {km.replace('.', ',')} km"
    return texto, categoria, raro


def valor_centavos(rng, categoria):
    """Sorteio no logaritmo: valores grandes são mais raros."""
    lo, hi = VALORES[categoria]
    v = math.exp(rng.uniform(math.log(lo), math.log(hi)))
    centavos = rng.choice([0, 0, rng.randrange(100)])
    return int(v) * 100 + centavos
