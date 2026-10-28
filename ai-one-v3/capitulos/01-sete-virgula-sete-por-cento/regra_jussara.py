import pandas as pd

TAXA = 0.045           # juros ao mês
DIVIDA = ("divid|dívid|agiota|cartão|cheque|nome|"
          "pendênc|atrasad")


def carteira():
    """Os empréstimos com o que a cobrança sabe de cada um."""
    emp = pd.read_csv("dados/brutos/emprestimos.csv",
                      parse_dates=["data_concessao"])
    cob = pd.read_csv("dados/brutos/cobranca.csv")
    return emp.merge(cob, on="pedido_id")


def regras_da_jussara(t):
    """As doze regras: uma coluna por regra, True se passa."""
    n = t["parcelas"]
    parcela = t["valor"] * TAXA / (1 - (1 + TAXA) ** -n)
    fat = t["faturamento_declarado"]
    novo = t["emprestimos_anteriores"] == 0
    online = t["canal"] == "online"
    festa = t["tipo_negocio"] == "ambulante de festas"
    texto = t["finalidade"].str.lower()
    return pd.DataFrame({
        "idade de 21 anos ou mais": t["idade"] >= 21,
        "idade de 70 anos ou menos": t["idade"] <= 70,
        "negócio com 6 meses ou mais":
            t["tempo_negocio_meses"] >= 6,
        "faturamento de R$ 800 ou mais": fat >= 800,
        "valor até 1,5 faturamento": t["valor"] <= 1.5 * fat,
        "parcela até 30% do faturamento":
            parcela <= 0.30 * fat,
        "nenhum atraso anterior": t["atrasos_anteriores"] == 0,
        "novo: até R$ 3.000": ~novo | (t["valor"] <= 3000),
        "novo: até 15 parcelas": ~novo | (n <= 15),
        "novo: atendido em pessoa": ~novo | ~online,
        "finalidade não é dívida": ~texto.str.contains(DIVIDA),
        "festa: até R$ 1.500": ~festa | (t["valor"] <= 1500),
    })


if __name__ == "__main__":
    t = carteira()
    t = t[t["data_concessao"].dt.year == 2025]
    regras = regras_da_jussara(t)
    print("regra                            recusaria")
    for nome in regras.columns:
        print(f"{nome:32} {(~regras[nome]).sum():9,}")

    aprova = regras.all(axis=1)
    noventa = t["data_atraso_90"].notna()
    todos = noventa.mean()
    aprovados = noventa[aprova].mean()
    recusados = noventa[~aprova].mean()
    print()
    print(f"empréstimos de 2025:  {len(t):,}")
    print(f"a regra aprovaria:    {aprova.sum():,}"
          f" ({aprova.mean():.0%})")
    print(f"chegaram a 90 dias:   {todos:.1%} de todos")
    print(f"  entre os aprovados: {aprovados:.1%}")
    print(f"  entre os recusados: {recusados:.1%}")
