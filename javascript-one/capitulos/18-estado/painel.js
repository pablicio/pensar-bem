function desenhar() {
  desenharListaNoDom(estado);
  document.querySelector("#detalhe").textContent =
    desenharDetalhe(estado);
  document.querySelector("#rodape").textContent =
    formatarReais(desenharRodape(estado));
}
