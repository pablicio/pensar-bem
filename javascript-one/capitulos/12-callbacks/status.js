function notificarCliente(e, depois) {
  setTimeout(() => {
    const falhou = true;
    if (falhou) {
      depois(new Error("WhatsApp: 503"));
      return;
    }
    depois(null);
  }, 300);
}

gravarStatus("E-5230", () => {
  notificarCliente("E-5230", (erro) => {
    if (erro) {
      console.log(`aviso não enviado: ${erro.message}`);
    }
    atualizarLinha("E-5230");
  });
});
