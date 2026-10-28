export function calcularFrete({ cidade, pesoKg, urgente = false }) {
  let base = 1290;
  if (cidade === "Franca") base = 1890;
  if (cidade === "São Carlos") base = 2290;
  if (cidade === "Ribeirão Preto") base = 1290;
  const extra = pesoKg > 5 ? Math.round((pesoKg - 5) * 90) : 0;
  return base + extra + (urgente ? 1000 : 0);
}
