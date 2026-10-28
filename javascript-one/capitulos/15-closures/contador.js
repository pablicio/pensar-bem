function criarContador(nome) {
  let total = 0;
  return function () {
    total++;
    console.log(`${nome}: ${total}`);
  };
}

const canceladas = criarContador("canceladas");
const entregues = criarContador("entregues");

canceladas();
canceladas();
entregues();
canceladas();
