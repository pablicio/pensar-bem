function buscarFrete(codigo) {
  return new Promise((resolver, rejeitar) => {
    setTimeout(() => {
      if (!codigo.startsWith("E-")) {
        rejeitar(new Error(`código inválido: ${codigo}`));
        return;
      }
      resolver(2340);
    }, 300);
  });
}

buscarFrete("5261")
  .then((frete) => console.log(`frete: ${frete}`))
  .catch((erro) => console.log(`falhou: ${erro.message}`));
