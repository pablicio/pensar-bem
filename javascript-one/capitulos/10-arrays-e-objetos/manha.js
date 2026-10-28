const codigos = manha.map((e) => e.codigo);
const ativas = manha.filter((e) => e.status !== "cancelada");
const e5141 = manha.find((e) => e.codigo === "E-5141");
const total = manha.reduce((soma, e) => soma + e.freteCentavos, 0);

console.log(codigos);
console.log(ativas.length);
console.log(e5141.status);
console.log(total);
