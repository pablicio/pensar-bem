const deFranca = [];
const semCidade = [];

for (const e of entregas) {
  if (!e.cidade) {
    semCidade.push(e.codigo);
    continue;
  }
  if (e.cidade === "Franca") {
    deFranca.push(e.codigo);
  }
}

console.log("Franca:", deFranca);
console.log("Sem cidade:", semCidade);
