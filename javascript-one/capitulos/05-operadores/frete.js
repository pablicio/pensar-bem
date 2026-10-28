function centavos(texto) {
  return Math.round(Number(texto.replace(",", ".")) * 100);
}

const total = centavos("10") + centavos("20");
console.log(total);
console.log(`R$ ${(total / 100).toFixed(2).replace(".", ",")}`);
