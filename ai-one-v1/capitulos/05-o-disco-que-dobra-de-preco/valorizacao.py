import matplotlib.pyplot as plt

v0 = 2400.0   # o que a loja pagou em 2019
v7 = 9000.0   # quanto vale em 2026, sete anos depois
anos = 7

passo = (v7 - v0) / anos              # linear: soma
taxa = (v7 / v0) ** (1 / anos) - 1    # exponencial: multiplica
print(f"linear: + R$ {passo:.2f} por ano")
print(f"exponencial: {taxa * 100:.2f}% ao ano")
print()
print("ano    linear  exponencial")
for t in range(anos + 1):
    linear = v0 + passo * t
    exponencial = v0 * (1 + taxa) ** t
    print(f"{2019 + t}  {linear:8.2f}  {exponencial:11.2f}")

ts = []
for i in range(0, 71):
    ts.append(i / 10)
lineares = []
exponenciais = []
for t in ts:
    lineares.append(v0 + passo * t)
    exponenciais.append(v0 * (1 + taxa) ** t)

plt.figure(figsize=(6, 3.5))
plt.plot(ts, lineares, linestyle="--", label="linear")
plt.plot(ts, exponenciais, label="exponencial")
plt.scatter([0, 7], [v0, v7])
plt.xlabel("anos desde 2019")
plt.ylabel("valor do disco (R$)")
plt.legend()
plt.savefig("valorizacao.png", dpi=300, bbox_inches="tight")
