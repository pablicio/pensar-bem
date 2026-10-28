import { test } from "node:test";
import assert from "node:assert/strict";
import { criarPainel } from "../painel.js";

function servidorLento(ms) {
  return {
    gravar: () => new Promise((r) => setTimeout(r, ms)),
  };
}

test("iniciar rota muda para a caminho", async () => {
  const painel = criarPainel(servidorLento(10), {
    "E-5701": "separada",
  });

  await painel.iniciarRota("E-5701");

  assert.equal(painel.status("E-5701"), "a caminho");
});

test("cancelar enquanto a rota ainda grava", async () => {
  const painel = criarPainel(servidorLento(50), {
    "E-5701": "separada",
  });

  const gravando = painel.iniciarRota("E-5701");
  await painel.cancelar("E-5701");
  await gravando;

  assert.equal(painel.status("E-5701"), "cancelada");
});
