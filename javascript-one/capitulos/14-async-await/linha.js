function falhar(mensagem, ms) {
  return new Promise((_, rejeitar) =>
    setTimeout(() => rejeitar(new Error(mensagem)), ms),
  );
}

async function marcarEntregue(codigo) {
  try {
    await buscar("gravado", 100);
    console.log(`${codigo}: gravado`);
    await falhar("WhatsApp: 503", 100);
    console.log(`${codigo}: notificado`);
  } catch (erro) {
    console.log(`${codigo}: ${erro.message}`);
  }
  console.log(`${codigo}: tela atualizada`);
}

marcarEntregue("E-5230");
