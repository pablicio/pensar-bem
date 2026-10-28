const lista = [{ codigo: "E-5188", endereco: "R. Tibiriçá, 440" }];

const d = { ...lista[0] };
d.endereco = "R. TIBIRIÇÁ, 440 — FUNDOS";

console.log(lista[0].endereco);
console.log(d.endereco);
console.log(d === lista[0]);
