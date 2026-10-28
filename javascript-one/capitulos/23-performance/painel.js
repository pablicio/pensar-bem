function mudarEntregas(novas) {
  estado.entregas = novas;
  desenharLista(estado);
  desenharRodape(estado);
}

function mudarAberta(codigo) {
  estado.aberta = codigo;
  desenharDetalhe(estado);
}

setInterval(() => {
  estado.agora = new Date();
  desenharRelogio(estado);
}, 1000);
