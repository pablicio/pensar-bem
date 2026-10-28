function criarAtualizador(codigo) {
  let rodadaAtual = 0;

  return async function atualizar(buscar) {
    rodadaAtual++;
    const minha = rodadaAtual;
    const dados = await buscar(codigo);
    if (minha !== rodadaAtual) {
      return;
    }
    console.log(`${codigo}: ${dados}`);
  };
}

const atualizarE5261 = criarAtualizador("E-5261");
