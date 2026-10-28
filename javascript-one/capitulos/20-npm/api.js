export function urlEntregas({ cidade, filtro }) {
  const params = new URLSearchParams({ cidade });
  if (filtro) {
    params.set("filtro", JSON.stringify(filtro));
  }
  return `/entregas?${params}`;
}

export async function buscarCanceladas(cidade) {
  const filtro = { status: "cancelada" };
  const url = urlEntregas({ cidade, filtro });
  const resposta = await fetch(url);
  return resposta.json();
}
