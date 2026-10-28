from pathlib import Path


def qual_encoding(caminho):
    """Um palpite: UTF-8 (com ou sem BOM) ou Latin-1."""
    dados = Path(caminho).read_bytes()
    if dados.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    try:
        dados.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        return "latin-1"


b = Path("dados/brutos")
nomes = ["inversores/corumba/corumba_2027-02.csv",
         "inversores/abadiania/abadiania_2027-02.csv",
         "ged/compensacao/compensacao_2027-02.csv",
         "ged/consumo/consumo_2027-02.csv",
         "envios/rateio_2027-02.csv"]
for nome in nomes:
    caminho = b / nome
    print(f"{qual_encoding(caminho):10} {caminho.name}")
