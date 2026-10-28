function processar(codigo, depois) {
  console.log(`processando ${codigo}`);
  depois(codigo);
}

function avisar(codigo) {
  console.log(`aviso: ${codigo} pronta`);
}

processar("E-5230", avisar);
