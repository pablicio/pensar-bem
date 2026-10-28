import shutil
from pathlib import Path

import openpyxl

# a pasta que o Wesley leva no notebook da usina
brutos = Path("dados/brutos")
copia = Path("dados/copia_wesley")
(copia / "envios").mkdir(parents=True, exist_ok=True)
for mes in ["2027-01", "2027-02"]:
    nome = f"envios/rateio_{mes}.csv"
    shutil.copy(brutos / nome, copia / nome)

# o cadastro, ele abriu para conferir um nome e salvou,
# sem mudar nenhuma célula
nome = "cadastro_cooperados.xlsx"
livro = openpyxl.load_workbook(brutos / nome)
livro.save(copia / nome)
print("cópia do Wesley em dados/copia_wesley/")
