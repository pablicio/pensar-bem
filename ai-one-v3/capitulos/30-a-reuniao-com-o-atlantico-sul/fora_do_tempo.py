from politicas import politicas

teste, valores, regras = politicas()
inicio = teste["data_concessao"].min()
fim = teste["data_concessao"].max()
print(f"teste: {len(teste):,} empréstimos, {inicio:%d/%m/%Y}"
      f" a {fim:%d/%m/%Y}\n")
print("política                 aprova inadimpl.      lucro")
for nome, aprova in regras.items():
    inad = teste["alvo"].to_numpy()[aprova].mean()
    print(f"{nome:24} {aprova.mean():6.1%} {inad:9.2%}"
          f" {valores[aprova].sum():10,.0f}")
