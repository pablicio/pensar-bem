function calcularFrete(cidade, pesoKg, urgente) {
  let base = 1290;
  if (cidade === "Franca") {
    base = 1890;
  }
  if (cidade === "São Carlos") {
    base = 2150;
  }

  let extra = 0;
  if (pesoKg > 5) {
    extra = Math.round((pesoKg - 5) * 90);
  }

  let frete = base + extra;
  if (urgente) {
    frete += 1000;
  }
  return frete;
}

console.log(calcularFrete("Franca", 8, false));
console.log(calcularFrete("São Carlos", 3, true));
console.log(calcularFrete("Ribeirão Preto", 12.5, false));
