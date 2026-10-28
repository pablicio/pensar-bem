def numero_br(texto):
    """'1.652,9' -> 1652.9; '--' (desligado) é erro."""
    texto = texto.strip()
    if texto == "--":
        raise ValueError("leitura vazia: inversor desligado")
    return float(texto.replace(".", "").replace(",", "."))


assert numero_br("1.652,9") == 1652.9
assert numero_br(" 936,0 ") == 936.0
try:
    numero_br("--")
except ValueError as erro:
    print("rejeitada:", erro)
