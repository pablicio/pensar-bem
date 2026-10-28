import json


def rodado_do_zero(caminho):
    """As células rodaram uma vez cada, de cima para baixo?"""
    with open(caminho, encoding="utf-8") as f:
        notebook = json.load(f)
    codigo = [c for c in notebook["cells"]
              if c["cell_type"] == "code"]
    contagem = [c["execution_count"] for c in codigo]
    esperado = list(range(1, len(codigo) + 1))
    return contagem == esperado, contagem


ok, contagem = rodado_do_zero("rateio.ipynb")
print("rodado do zero:", ok, contagem)
