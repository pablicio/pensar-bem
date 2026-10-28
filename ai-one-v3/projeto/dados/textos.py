"""O campo "para que é o dinheiro", como o cliente fala."""
from mundo import rng

FINALIDADES = {
    "capital de giro": [
        "capital de giro", "capital de giro pro negocio",
        "giro do negócio", "dinheiro pra girar",
        "reforçar o caixa", "caixa do mes", "pagar fornecedor",
        "segurar o mes fraco", "capital de giro mesmo",
        "pra rodar o negocio", "giro", "ajuda no caixa",
        "comprar e revender", "manter o negócio girando",
    ],
    "estoque": [
        "comprar mercadoria", "estoque", "repor estoque",
        "comprar tecido", "comprar mercadoria pro natal",
        "aumentar o estoque", "mercadoria pra feira",
        "comprar material", "repor mercadoria",
        "estoque pro verão", "comprar no atacado",
    ],
    "equipamento": [
        "comprar maquina de costura", "freezer novo",
        "maquininha e balcão", "cadeira de barbeiro",
        "comprar ferramenta", "equipamento",
        "chapa e fritadeira",
        "trocar o carrinho", "comprar uma moto pra entrega",
        "isopor e guarda sol", "secador e chapinha",
    ],
    "reforma": [
        "reforma do ponto", "reformar a loja",
        "pintar o salão", "fazer a fachada", "obra no ponto",
        "consertar o telhado",
        "ajeitar o espaço", "reforma do quiosque",
    ],
    "pagar dívida": [
        "quitar o cartão", "pagar umas contas atrasadas",
        "acertar com o agiota", "fechar umas contas",
        "organizar as dividas", "pagar o cheque especial",
        "cobrir um empréstimo", "limpar o nome",
        "acertar umas pendências",
        "pagar conta de luz atrasada",
    ],
}
PESOS = {"capital de giro": 0.42, "estoque": 0.22,
         "equipamento": 0.14, "reforma": 0.10,
         "pagar dívida": 0.12}


def escreve(categoria):
    """Uma frase da categoria, às vezes com um enfeite."""
    frase = rng.choice(FINALIDADES[categoria])
    u = rng.random()
    if u < 0.15:
        frase = frase.upper()
    elif u < 0.25:
        frase = frase + " urgente"
    elif u < 0.32:
        frase = "é pra " + frase
    return str(frase)
