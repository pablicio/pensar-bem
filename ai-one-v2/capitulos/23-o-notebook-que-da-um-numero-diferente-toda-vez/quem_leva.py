from rateio.leitura import ler_cadastro
from rateio.limpeza import cpf_normalizado

cad = ler_cadastro()
usina = cad[(cad["Situação"] == "Ativo")
            & (cad["Usina"] == "Abadiânia")]
nomes = dict(zip(cpf_normalizado(usina["CPF"]), usina["Nome"]))
cpfs = set(nomes)
quem = next(iter(cpfs))      # "o primeiro" do conjunto
print(f"a sobra de Abadiânia vai para {nomes[quem]}")
