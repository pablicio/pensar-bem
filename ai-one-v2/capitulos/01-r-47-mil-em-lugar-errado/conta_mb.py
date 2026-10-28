from pathlib import Path

brutos = Path("dados/brutos")
fontes = {
    "Corumbá (A)": "inversores/corumba/*.csv",
    "Cocalzinho (B)": "inversores/cocalzinho/*.json",
    "Abadiânia (C)": "inversores/abadiania/*.csv",
}
for nome, padrao in fontes.items():
    tamanho = 0
    for arquivo in brutos.glob(padrao):
        tamanho += arquivo.stat().st_size
    print(f"{nome:16} {tamanho / 1_048_576:7.1f} MB")
