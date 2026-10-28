from rateio import manifesto

antes = manifesto.ler("dados/manifesto_brutos.json")
agora = manifesto.gerar("dados/brutos")
mudou = manifesto.comparar(antes, agora)
for tipo, arquivos in mudou.items():
    print(f"{tipo}: {len(arquivos)}", *arquivos)
if any(mudou.values()):
    raise SystemExit("os dados brutos mudaram")
print("dados brutos conferidos com o manifesto")
