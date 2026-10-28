export function calcularFrete({ cidade, pesoKg, urgente = false }) {
  let base = 1290;
  if (cidade === "Franca") base = 1890;
  if (cidade === "São Carlos") base = 2150;
  const extra = pesoKg > 5 ? Math.round((pesoKg - 5) * 90) : 0;
  return base + extra + (urgente ? 1000 : 0);
}

export function formatarReais(centavos) {
  const texto = (centavos / 100).toFixed(2);
  return `R$ ${texto.replace(".", ",")}`;
}
