from roda_celulas import roda

com = roda([1, 2, 3, 4, 5, 6])["credito"].sum()
sem = roda([1, 2, 3, 5, 6])["credito"].sum()
print(f"sem a célula 4: R$ {sem:,.2f}")
print(f"com a célula 4: R$ {com:,.2f}")
print(f"a perda tirou:  R$ {sem - com:,.2f}")
