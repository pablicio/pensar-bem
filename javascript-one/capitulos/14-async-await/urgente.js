async function buscarFrete(codigo) {
  return 2340;
}

async function freteDaLinha(e) {
  const frete = buscarFrete(e.codigo) + (e.urgente ? 1000 : 0);
  return frete;
}

freteDaLinha({ codigo: "E-5302", urgente: true })
  .then((f) => console.log(`R$ ${f}`));
