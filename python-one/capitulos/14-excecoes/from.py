try:
    dados = json.loads(corpo)
except json.JSONDecodeError as erro:
    raise ErroDoCatalogo("corpo inválido") from erro
