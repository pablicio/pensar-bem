const e = { entregue: true, cancelada: true };

let rotulo = "a caminho";
if (e.entregue) {
  rotulo = "entregue";
}
if (e.cancelada) {
  rotulo = "cancelada";
}
console.log(rotulo);
