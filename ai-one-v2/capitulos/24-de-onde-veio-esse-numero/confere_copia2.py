from pathlib import Path

from rateio import manifesto

nota = Path("dados/copia_wesley/anotacoes.txt")
nota.write_text("Seu Geraldo: ligar depois das 18h\n",
                encoding="utf-8")

registrado = manifesto.ler("dados/manifesto_brutos.json")
copia = manifesto.gerar("dados/copia_wesley")
for nome, sha in copia.items():
    if nome not in registrado:
        print("NÃO ESTÁ NO MANIFESTO", nome)
    elif registrado[nome] == sha:
        print("igual                ", nome)
    else:
        print("DIFERENTE            ", nome)
