import { SITUACOES } from "./situacoes.js";

const ORDEM = SITUACOES.map((s, i) => [s, i]);

export function desenharLinha(e) {
  return `${e.codigo} ${e.status}`;
}
