const express = require("express");

const API_URL = process.env.API_URL;
if (!API_URL) {
  console.error("falta a variável API_URL");
  process.exit(1);
}

const app = express();

app.get("/validar/:codigo", async (req, res) => {
  const url = `${API_URL}/ingressos/${req.params.codigo}`;
  const r = await fetch(url);
  res.status(r.status).json(await r.json());
});

const servidor = app.listen(3000, "0.0.0.0", () =>
  console.log("check-in escutando na 3000"));

process.on("SIGTERM", () => {
  servidor.close(() => process.exit(0));
});
