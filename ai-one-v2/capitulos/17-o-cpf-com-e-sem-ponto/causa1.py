import pandas as pd


def digitos(serie):
    return serie.str.replace(r"\D", "", regex=True)


envio = pd.read_csv("dados/brutos/envios/rateio_2027-02.csv",
                    sep=";", decimal=",", thousands=".",
                    dtype={"CPF": "string"})
ged = pd.read_csv("dados/brutos/ged/compensacao/"
                  "compensacao_2027-02.csv", sep=";",
                  encoding="latin-1", decimal=",",
                  thousands=".", dtype={"CPF": "string"})

aplicado = ged.set_index(digitos(ged["CPF"]))["Valor (R$)"]
enviado = digitos(envio["CPF"])
envio["aplicado"] = enviado.str.zfill(11).map(aplicado)
curtos = envio[enviado.str.len() != 11]

if __name__ == "__main__":
    print(len(curtos), "CPFs enviados com menos de 11 dígitos")
    print(curtos.sort_values("Valor", ascending=False)
          [["CPF", "Nome", "Valor", "aplicado"]].head(3))
    enviado_r, aplicado_r = curtos[["Valor", "aplicado"]].sum()
    print(f"enviado a eles:  R$ {enviado_r:9,.2f}")
    print(f"aplicado a eles: R$ {aplicado_r:9,.2f}")
