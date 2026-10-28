# três linhas do arquivo de fevereiro do fabricante A
linha1 = "01/02/2027;11:00;INV-01;1.652,9"
linha2 = "08/02/2027;12:00;INV-10;936,0"
linha3 = "10/02/2027;12:00;INV-10;1,0473"

texto1 = linha1.split(";")[3]
texto2 = linha2.split(";")[3]
texto3 = linha3.split(";")[3]

valor1 = float(texto1.replace(".", "").replace(",", "."))
valor2 = float(texto2.replace(".", "").replace(",", "."))
valor3 = float(texto3.replace(".", "").replace(",", "."))

troca = str.maketrans(",.", ".,")
print(f"{texto1!r:>10} -> {valor1:9.4f} -> "
      f"{f'{valor1:,.1f}'.translate(troca)}")
print(f"{texto2!r:>10} -> {valor2:9.4f} -> "
      f"{f'{valor2:,.1f}'.translate(troca)}")
print(f"{texto3!r:>10} -> {valor3:9.4f} -> "
      f"{f'{valor3:,.1f}'.translate(troca)}")
