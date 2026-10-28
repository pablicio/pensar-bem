from rateio.leitura import ler_corumba

a = ler_corumba("2027-02")
dia = a[(a["Data"] == "10/02/2027")
        & (a["Inversor"] == "INV-12")]
ate_a_foto = dia[dia["Hora"] < "14:35"]
soma = ate_a_foto["Energia"].sum()
print(f"soma do arquivo até 14h35: {soma:.4f}")
print(f"se fossem Wh:  {soma / 1000:.4f} kWh")
print(f"se fossem kWh: {soma:.1f} kWh   (visor: 103,0 kWh)")
