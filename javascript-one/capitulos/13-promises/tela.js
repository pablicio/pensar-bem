let rodadaAtual = 0;

function atualizar(status, frete, msStatus, msFrete) {
  rodadaAtual++;
  const minha = rodadaAtual;

  Promise.all([buscar(status, msStatus), buscar(frete, msFrete)])
    .then(([s, f]) => {
      if (minha !== rodadaAtual) {
        console.log(`${t()} rodada ${minha} descartada`);
        return;
      }
      linha.status = s;
      linha.frete = f;
      mostrar(`rodada ${minha}`);
    });
}

atualizar("a caminho", 1890, 120, 450);
setTimeout(() => atualizar("entregue", 2340, 120, 60), 200);
