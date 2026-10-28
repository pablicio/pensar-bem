const entregas = [
  { codigo: "E-5030", cidade: "Franca", frete: 1890 },
  { codigo: "E-5031", cidade: "Franca", frete: 2300 },
  { codigo: "E-5032", cidade: "São Carlos", frete: 1550 },
];

let total = 0;
let deFranca = 0;
const codigos = [];

for (const e of entregas) {
  total += e.frete;
  if (e.cidade === "Franca") {
    deFranca++;
  }
  codigos.push(e.codigo);
}

console.log(total, deFranca, codigos);
