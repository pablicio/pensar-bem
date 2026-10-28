produtos = session.scalars(select(Produto).limit(100)).all()

for p in produtos:
    print(p.nome, p.produtor.nome)
