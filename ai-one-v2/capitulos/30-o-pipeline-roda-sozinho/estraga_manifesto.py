from rateio import manifesto

m = manifesto.ler("dados/manifesto_brutos.json")
m["cadastro_cooperados.xlsx"] = "0" * 64
manifesto.gravar(m, "dados/manifesto_teste.json")
print("manifesto de teste com o cadastro adulterado")
