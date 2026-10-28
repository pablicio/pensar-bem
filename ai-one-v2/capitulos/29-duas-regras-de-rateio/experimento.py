import pandas as pd

from rateio import registro
from rateio.calculo import TARIFA
from rateio.leitura import BRUTOS, ler_cadastro
from rateio.limpeza import cpf_normalizado

GERACAO = "dados/processados/geracao_diaria.csv"
CONSUMO = BRUTOS / "ged/consumo"
MESES = [str(m) for m in pd.period_range("2026-03", "2027-02",
                                         freq="M")]
ENTRADAS = [GERACAO, BRUTOS / "cadastro_cooperados.xlsx"] + [
    CONSUMO / f"consumo_{mes}.csv" for mes in MESES]


def monta_tabela():
    """Uma linha por cooperado e mês, com geração e consumo."""
    g = pd.read_csv(GERACAO)
    geracao = g.groupby([g["data"].str[:7], "usina"])["kwh"]
    geracao = geracao.sum().round(3)
    cad = ler_cadastro()
    ativos = cad[cad["Situação"] == "Ativo"]
    base = pd.DataFrame({"cpf": cpf_normalizado(ativos["CPF"]),
                         "usina": ativos["Usina"],
                         "tipo": ativos["Tipo"],
                         "cota": ativos["Cota (%)"]})
    partes = []
    for mes in MESES:
        c = pd.read_csv(CONSUMO / f"consumo_{mes}.csv",
                        dtype={"cpf": "string"})
        cpf = cpf_normalizado(c["cpf"])
        consumo = c.groupby(cpf)["kwh"].sum()
        t = base.assign(mes=mes)
        t["consumo"] = t["cpf"].map(consumo).fillna(0)
        da_usina = geracao[mes].reindex(t["usina"])
        t["geracao"] = da_usina.to_numpy()
        partes.append(t)
    return pd.concat(partes, ignore_index=True)


def credito_kwh(t, p):
    """Fração p da geração pelo consumo; o resto, pela cota."""
    por_cota = t["geracao"] * t["cota"] / 100
    consumo_usina = t.groupby(["mes", "usina"])["consumo"]
    por_consumo = (t["geracao"] * t["consumo"]
                   / consumo_usina.transform("sum"))
    return ((1 - p) * por_cota + p * por_consumo).round(2)


def metricas(t, p):
    """As três métricas combinadas antes dos resultados."""
    kwh = credito_kwh(t, p)
    ano = pd.DataFrame({
        "cpf": t["cpf"], "kwh": kwh, "consumo": t["consumo"],
        "reais": (kwh * TARIFA).round(2),
        "atual": (credito_kwh(t, 0) * TARIFA).round(2),
    }).groupby("cpf").sum()
    parado = (ano["kwh"] - ano["consumo"]).clip(lower=0).sum()
    muda = (ano["reais"] - ano["atual"]).abs().sum() / 2
    perdem = (ano["reais"] < 0.9 * ano["atual"]).sum()
    return {"credito_parado": round(float(parado * TARIFA), 2),
            "muda_de_mao": round(float(muda), 2),
            "perdem_mais_de_10pct": int(perdem)}


if __name__ == "__main__":
    tabela = monta_tabela()
    n = tabela["cpf"].nunique()
    print(f"{len(tabela):,} linhas: {n:,} cooperados"
          f" x {len(MESES)} meses")
    for nome, p in [("por cota", 0.0), ("por consumo", 1.0)]:
        m = metricas(tabela, p)
        registro.registrar("regra de rateio", {"p_consumo": p},
                           m, ENTRADAS)
        print(f"{nome}:")
        for metrica, valor in m.items():
            print(f"  {metrica:22} {valor:>14,}")
