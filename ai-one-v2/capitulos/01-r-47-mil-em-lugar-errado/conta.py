from pathlib import Path

LIMITE_EXCEL = 1_048_576          # linhas de uma aba do Excel
brutos = Path("dados/brutos")
fontes = {
    "Corumbá (A)": "inversores/corumba/*.csv",
    "Cocalzinho (B)": "inversores/cocalzinho/*.json",
    "Abadiânia (C)": "inversores/abadiania/*.csv",
    "consumo da GED": "ged/consumo/*.csv",
    "compensação GED": "ged/compensacao/*.csv",
}
for nome, padrao in fontes.items():
    arquivos = sorted(brutos.glob(padrao))
    linhas = 0
    for arquivo in arquivos:
        conteudo = arquivo.read_bytes()
        if arquivo.suffix == ".json":
            linhas += conteudo.count(b'"inversor"')
        else:
            linhas += conteudo.count(b"\n")
    cabe = linhas <= LIMITE_EXCEL
    aviso = "" if cabe else "  não cabe no Excel"
    print(f"{nome:16} {len(arquivos):3} arquivos "
          f"{linhas:11,} linhas{aviso}")
