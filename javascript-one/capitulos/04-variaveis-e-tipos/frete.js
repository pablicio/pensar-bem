const frete = 1890;
const retorno = 720;
const total = frete + retorno;

console.log(total);
console.log(total === 2610);
console.log(`R$ ${(total / 100).toFixed(2).replace(".", ",")}`);
