from pathlib import Path

from validacao import CPFInvalido, confere_cpf

pasta = Path("dados/brutos/ged/consumo")
for caminho in sorted(pasta.glob("*.csv")):
    lidas = 0
    ruins = 0
    with open(caminho, encoding="utf-8") as entrada:
        entrada.readline()
        for linha in entrada:
            lidas += 1
            data, cpf, kwh = linha.strip().split(",")
            try:
                confere_cpf(cpf)
                float(kwh)
            except (CPFInvalido, ValueError):
                ruins += 1
    print(f"{caminho.name}  {lidas:6} lidas  "
          f"{ruins} rejeitadas")
