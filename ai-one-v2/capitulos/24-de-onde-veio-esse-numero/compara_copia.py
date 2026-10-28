import pandas as pd

nome = "cadastro_cooperados.xlsx"
original = pd.read_excel(f"dados/brutos/{nome}",
                         dtype={"CPF": "string"})
da_copia = pd.read_excel(f"dados/copia_wesley/{nome}",
                         dtype={"CPF": "string"})
print("mesmos dados:", original.equals(da_copia))
