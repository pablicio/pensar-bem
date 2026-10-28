const SITUACOES = {
  ENTREGUE: "entregue",
  "EM ROTA": "a caminho",
  CANCELADA: "cancelada",
};

function doSistemaAntigo(a) {
  const status = SITUACOES[a.situacao];
  if (status === undefined) {
    throw new Error(`${a.codigo}: situação ${a.situacao}`);
  }
  return {
    codigo: a.codigo,
    status: status,
    cidade: a.municipio.charAt(0)
      + a.municipio.slice(1).toLowerCase(),
    freteCentavos: Math.round(
      Number(a.frete.replace(",", ".")) * 100,
    ),
  };
}

function doAplicativo(n) {
  return {
    codigo: n.id,
    status: n.status,
    cidade: n.cidade,
    freteCentavos: n.freteCentavos,
  };
}

const antiga = {
  codigo: "E-5140", situacao: "ENTREGUE",
  municipio: "FRANCA", frete: "21,60",
};
const nova = {
  id: "E-5140", status: "entregue",
  cidade: "Franca", freteCentavos: 2160,
};

console.log(doSistemaAntigo(antiga));
console.log(doAplicativo(nova));
