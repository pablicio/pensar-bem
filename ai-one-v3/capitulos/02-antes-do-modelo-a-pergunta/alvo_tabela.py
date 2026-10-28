from risco.alvo import carteira, com_alvo, maduros

t = carteira()
m = maduros(t)
prazo = (m["data_atraso_90"] - m["data_concessao"]).dt.days
definicoes = {
    "30 dias, alguma vez": m["data_atraso_30"].notna(),
    "90 dias, alguma vez": m["data_atraso_90"].notna(),
    "90 dias em até 12 meses": prazo <= 365,
}
print(f"empréstimos no extrato:  {len(t):,}")
print(f"maduros (até 12/3/2026): {len(m):,}")
print()
for nome, positivo in definicoes.items():
    n, taxa = positivo.sum(), positivo.mean()
    print(f"{nome:24} {n:6,}  {taxa:6.1%}")

treino = com_alvo(t)
print()
print(f"tabela de treino: {len(treino):,} linhas,"
      f" {treino['alvo'].sum():,} positivos")
