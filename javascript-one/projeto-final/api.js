export async function gravarStatus(codigo, status) {
  const resposta = await fetch(`/entregas/${codigo}/status`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });

  const corpo = await resposta.json();
  if (!resposta.ok) {
    const erro = new Error(corpo.erro);
    erro.status = resposta.status;
    erro.corpo = corpo;
    throw erro;
  }
  return corpo;
}
