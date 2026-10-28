const entregas = [
  { codigo: "E-5030", cidade: "Franca" },
  { codigo: "E-5031", cidade: "Franca" },
  { codigo: "E-5032", cidade: "Franca" },
  { codigo: "E-5033", cidade: "" },
];

for (const e of entregas) {
  console.log(`${e.codigo} | ${e.cidade}`);
}
