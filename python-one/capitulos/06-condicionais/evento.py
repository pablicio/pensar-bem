evento = {"tipo": "entrega", "caixas": 12}

match evento:
    case {"tipo": "entrega", "caixas": int(n)} if n > 10:
        print(f"entrega grande: {n} caixas")
    case {"tipo": "entrega"}:
        print("entrega comum")
    case {"tipo": "devolucao"}:
        print("devolução")
