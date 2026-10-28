lista.addEventListener("click", (evento) => {
  const botao = evento.target.closest("button[data-codigo]");
  if (!botao) {
    return;
  }
  cancelar(botao.dataset.codigo);
});

function desenhar(entregas) {
  lista.replaceChildren();
  for (const codigo of entregas) {
    const item = document.createElement("li");
    const botao = document.createElement("button");
    botao.textContent = "cancelar";
    botao.dataset.codigo = codigo;
    item.append(codigo, " ", botao);
    lista.append(item);
  }
}
