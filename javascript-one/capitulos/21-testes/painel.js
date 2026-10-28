async function iniciarRota(codigo) {
  const antes = entregas.get(codigo);
  await servidor.gravar(codigo, "a caminho");
  if (entregas.get(codigo) !== antes) {
    return;
  }
  entregas.set(codigo, "a caminho");
}
