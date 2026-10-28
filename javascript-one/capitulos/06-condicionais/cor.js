function cor(situacao) {
  switch (situacao) {
    case "a caminho":
      return "azul";
    case "entregue":
      return "verde";
    case "cancelada":
      return "cinza";
    default:
      throw new Error(`situação desconhecida: ${situacao}`);
  }
}

console.log(cor("entregue"));
