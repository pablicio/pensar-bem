import { createServer } from "node:http";

const STATUS = ["SEPARADA", "EM_ROTA", "ENTREGUE", "CANCELADA"];
const entregas = new Map([["E-5801", "SEPARADA"]]);

function responder(res, codigo, corpo) {
  res.writeHead(codigo, { "Content-Type": "application/json" });
  res.end(JSON.stringify(corpo));
}

const servidor = createServer(async (req, res) => {
  const achou = req.url.match(/^\/entregas\/(E-\d+)\/status$/);
  if (req.method !== "PUT" || !achou) {
    return responder(res, 404, { erro: "rota inexistente" });
  }

  let texto = "";
  for await (const pedaco of req) texto += pedaco;
  const { status } = JSON.parse(texto);

  if (!STATUS.includes(status)) {
    return responder(res, 422, {
      erro: "status inválido",
      campo: "status",
      recebido: status,
      aceitos: STATUS,
    });
  }

  const codigo = achou[1];
  if (entregas.get(codigo) === "CANCELADA") {
    return responder(res, 409, { erro: "entrega já cancelada" });
  }
  entregas.set(codigo, status);
  responder(res, 200, { codigo, status });
});

servidor.listen(3000, () => console.log("servidor em :3000"));
