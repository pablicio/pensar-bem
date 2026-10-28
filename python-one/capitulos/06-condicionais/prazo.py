tipo = "PIX"

match tipo:
    case "PIX":
        prazo = "imediato"
    case "CARTAO":
        prazo = "2 dias"
    case "BOLETO" | "TED":
        prazo = "3 dias úteis"
    case _:
        prazo = "desconhecido"

print(prazo)
