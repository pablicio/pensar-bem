import { SITUACOES } from "./situacoes.js";
import { desenharLinha } from "./lista.js";

export function cancelar(e) {
  if (!SITUACOES.includes(e.status)) {
    throw new Error(`${e.codigo}: situação ${e.status}`);
  }
  return desenharLinha({ ...e, status: "cancelada" });
}
