import { test } from "node:test";
import assert from "node:assert/strict";
import { calcularFrete } from "../frete.js";

test("Franca, 8 kg, sem urgência", () => {
  const frete = calcularFrete({ cidade: "Franca", pesoKg: 8 });
  assert.equal(frete, 2160);
});
