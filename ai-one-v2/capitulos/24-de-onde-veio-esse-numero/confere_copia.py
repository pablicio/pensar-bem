from rateio import manifesto

registrado = manifesto.ler("dados/manifesto_brutos.json")
copia = manifesto.gerar("dados/copia_wesley")
for nome, sha in copia.items():
    igual = registrado.get(nome) == sha
    print("igual    " if igual else "DIFERENTE", nome)
