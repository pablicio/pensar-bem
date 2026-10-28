function lerPendencias(texto) {
  if (texto === "" || texto === null || texto === undefined) {
    return null;
  }
  return Number(texto);
}

const pendencias = lerPendencias("");
console.log(pendencias === 0 ? "liberada" : "segura");
