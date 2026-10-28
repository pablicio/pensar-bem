from rateio.leituras import leituras_do_mes

leituras = leituras_do_mes("2027-03")
print(leituras.dtypes.to_string())
memoria = leituras.memory_usage(deep=True) / 1e6
print(memoria.round(1).to_string())
print(f"total: {memoria.sum():.1f} MB")
