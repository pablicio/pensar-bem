const original = {
  codigo: "E-5188",
  destino: { rua: "R. Tibiriçá", numero: 440 },
};

const copia = { ...original };
copia.codigo = "E-5188-B";
copia.destino.numero = 442;

console.log(original.codigo);
console.log(original.destino.numero);
