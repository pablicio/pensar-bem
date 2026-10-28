const inicio = Date.now();
const t = () => `${String(Date.now() - inicio).padStart(4)} ms`;

function buscar(valor, ms) {
  return new Promise((r) => setTimeout(() => r(valor), ms));
}

let rodadaAtual = 0;

async function atualizar(status, frete, msStatus, msFrete) {
  rodadaAtual++;
  const minha = rodadaAtual;

  const [s, f] = await Promise.all([
    buscar(status, msStatus),
    buscar(frete, msFrete),
  ]);

  if (minha !== rodadaAtual) {
    console.log(`${t()} rodada ${minha} descartada`);
    return;
  }
  console.log(`${t()} rodada ${minha}: ${s} | ${f}`);
}

atualizar("a caminho", 1890, 120, 450);
setTimeout(() => atualizar("entregue", 2340, 120, 60), 200);
