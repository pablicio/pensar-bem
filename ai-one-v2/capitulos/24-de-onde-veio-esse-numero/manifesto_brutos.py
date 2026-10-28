from rateio import manifesto

m = manifesto.gerar("dados/brutos")
manifesto.gravar(m, "dados/manifesto_brutos.json")
print(f"{len(m)} arquivos em dados/manifesto_brutos.json")
envio = m["envios/rateio_2027-02.csv"]
print("envios/rateio_2027-02.csv:", envio[:16], "...")
