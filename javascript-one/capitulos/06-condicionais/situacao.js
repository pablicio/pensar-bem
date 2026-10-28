function situacao(e) {
  if (e.entregue && e.cancelada) {
    throw new Error(`${e.codigo}: entregue e cancelada`);
  }
  if (e.cancelada) {
    return "cancelada";
  }
  if (e.entregue) {
    return "entregue";
  }
  return "a caminho";
}

console.log(situacao({ codigo: "E-5010", entregue: true }));
console.log(situacao({ codigo: "E-5011" }));
const e5012 = { codigo: "E-5012", entregue: true, cancelada: true };
console.log(situacao(e5012));
