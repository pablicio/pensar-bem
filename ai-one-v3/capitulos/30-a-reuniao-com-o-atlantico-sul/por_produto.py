from politicas import politicas

teste, valores, regras = politicas()
alvo = teste["alvo"].to_numpy()
for produto in ["Capital de giro", "MEI Mais"]:
    s = (teste["produto"] == produto).to_numpy()
    print(f"{produto} ({s.sum():,} empréstimos)")
    for nome, aprova in regras.items():
        a = s & aprova
        lucro = valores[a].sum()
        print(f"  {nome:24} {a.sum() / s.sum():6.1%}"
              f" {alvo[a].mean():7.2%} {lucro:9,.0f}")
