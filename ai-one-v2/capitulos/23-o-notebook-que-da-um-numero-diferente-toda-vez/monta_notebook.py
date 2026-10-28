import json

C1 = """\
import random
import pandas as pd"""

C2 = """\
cad = pd.read_excel("dados/brutos/cadastro_cooperados.xlsx",
                    dtype={"CPF": "string"})
ativos = cad[cad["Situação"] == "Ativo"]"""

C3 = """\
# fevereiro/2027, kWh, do relatório da GED
GERACAO = {"Corumbá de Goiás": 259313.777,
           "Cocalzinho": 186790.392,
           "Abadiânia": 126809.824}
TARIFA = 0.9412
PERDA = 0.0045  # perda na rede"""

C4 = """\
for usina in GERACAO:
    GERACAO[usina] = GERACAO[usina] * (1 - PERDA)"""

C5 = """\
geracao = ativos["Usina"].map(GERACAO)
kwh = (geracao * ativos["Cota (%)"] / 100).round(2)
credito = (kwh * TARIFA).round(2)"""

C6 = """\
# a sobra do arredondamento, centavo a centavo, para
# cooperados sorteados da usina
for usina, g in GERACAO.items():
    da_usina = ativos.index[ativos["Usina"] == usina]
    sobra = g * TARIFA - credito[da_usina].sum()
    centavos = round(sobra * 100)
    passo = 0.01 if centavos > 0 else -0.01
    for i in random.sample(list(da_usina), abs(centavos)):
        credito[i] = round(credito[i] + passo, 2)"""

C7 = """\
dirceu = ativos["Código"] == 2959  # o Seu Dirceu
print(f"Dirceu: R$ {credito[dirceu].iloc[0]:,.2f}")"""

# como o Matheus deixou: o número de execução de cada célula
# e a última saída da célula 7
CONTAGEM = [1, 2, 3, 8, 9, 10, 11]
SAIDA = "Dirceu: R$ 1,643.07\n"

celulas = []
for n, (fonte, conta) in enumerate(
        zip([C1, C2, C3, C4, C5, C6, C7], CONTAGEM), start=1):
    saidas = []
    if n == 7:
        saidas = [{"output_type": "stream", "name": "stdout",
                   "text": SAIDA}]
    celulas.append({"cell_type": "code", "id": f"c{n}",
                    "execution_count": conta, "metadata": {},
                    "source": fonte, "outputs": saidas})

notebook = {"cells": celulas, "nbformat": 4,
            "nbformat_minor": 5,
            "metadata": {"language_info": {"name": "python"}}}
with open("rateio.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)
print(len(celulas), "células gravadas em rateio.ipynb")
