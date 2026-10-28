async function gravarStatus(codigo, status) {
  const resposta = await fetch(
    `http://localhost:3000/entregas/${codigo}/status`,
    {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    },
  );
  const corpo = await resposta.json();
  console.log(resposta.status, corpo);
}

await gravarStatus("E-5801", "cancelado");
await gravarStatus("E-5801", "CANCELADA");
await gravarStatus("E-5801", "EM_ROTA");
