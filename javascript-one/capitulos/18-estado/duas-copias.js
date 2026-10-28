const lista = [
  { codigo: "E-5512", status: "a caminho", frete: 1890 },
  { codigo: "E-5513", status: "a caminho", frete: 2160 },
];

const detalhe = { ...lista[0] };
let totalRodape = lista.reduce((s, e) => s + e.frete, 0);

function desenhar() {
  const linhas = lista.map((e) => `${e.codigo} ${e.status}`);
  console.log(`lista:   ${linhas.join(" | ")}`);
  console.log(`detalhe: ${detalhe.codigo} ${detalhe.status}`);
  console.log(`rodapé:  ${totalRodape}`);
}

lista[0].status = "cancelada";
desenhar();
