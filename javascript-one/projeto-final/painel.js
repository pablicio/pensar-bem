export function criarPainel(servidor, inicial) {
  const entregas = new Map(Object.entries(inicial));

  function status(codigo) {
    return entregas.get(codigo);
  }

  async function iniciarRota(codigo) {
    await servidor.gravar(codigo, "a caminho");
    entregas.set(codigo, "a caminho");
  }

  async function cancelar(codigo) {
    entregas.set(codigo, "cancelada");
    await servidor.gravar(codigo, "cancelada");
  }

  return { status, iniciarRota, cancelar };
}
