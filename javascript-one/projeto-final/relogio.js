const entregas = Array.from({ length: 160 }, (_, i) => ({
  codigo: `E-${5900 + i}`,
  status: "a caminho",
}));

let cartoesCriados = 0;

function desenharLista() {
  for (const e of entregas) {
    cartoesCriados++;
    // no navegador: criar o <li>, o botão, pôr na página
  }
}

function desenharRelogio(segundo) {
  return `atualizado às 6h05:${String(segundo).padStart(2, "0")}`;
}

// como estava: cada segundo do relógio redesenha tudo
for (let s = 0; s < 60; s++) {
  desenharLista();
  desenharRelogio(s);
}
console.log(`antes: ${cartoesCriados} cartões em 60 s`);

// como fica: a lista uma vez, o relógio sozinho
cartoesCriados = 0;
desenharLista();
for (let s = 0; s < 60; s++) {
  desenharRelogio(s);
}
console.log(`depois: ${cartoesCriados} cartões em 60 s`);
