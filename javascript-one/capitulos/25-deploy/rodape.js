const entregas = [
  { codigo: "E-6001", cidade: "Franca", frete: 1890 },
  { codigo: "E-6002", cidade: "Franca", frete: 2160 },
  { codigo: "E-6003", cidade: "São Carlos", frete: 2290 },
];

const porCidade = Object.groupBy(entregas, (e) => e.cidade);

for (const [cidade, lista] of Object.entries(porCidade)) {
  const total = lista.reduce((s, e) => s + e.frete, 0);
  console.log(`${cidade}: ${lista.length} entrega(s), ${total}`);
}
