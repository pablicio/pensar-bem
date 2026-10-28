function freteAntigo(e) {
  var base = 1290;
  if (e.cidade == "Franca") base = 1890;
  if (e.cidade == "São Carlos") base = 2150;
  var extra = 0;
  if (e.peso > 5) extra = Math.round((e.peso - 5) * 90);
  var frete = base + extra;
  if (e.urgente) frete = frete + 1000;
  return frete;
}

// semana: as entregas exportadas da produção
let diferentes = 0;
for (const e of semana) {
  const novo = calcularFrete(e.cidade, e.peso, e.urgente);
  if (novo !== freteAntigo(e)) {
    diferentes++;
    console.log(e.codigo, novo, freteAntigo(e));
  }
}
console.log(`${semana.length} entregas, ${diferentes} diferentes`);
