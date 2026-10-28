import { doSistemaAntigo } from "./situacoes.js";
import { calcularFrete, formatarReais } from "./frete.js";

const papel = [
  "E-6201 | Franca | a caminho | R$ 21,60",
  "E-6202 | São Carlos | cancelada | R$ 22,90",
  "E-6203 | (sem cidade) | a caminho | R$ 12,90",
];

const sistemaAntigo = [
  { codigo: "E-6201", situacao: "EM ROTA", municipio: "FRANCA",
    peso: 8 },
  { codigo: "E-6202", situacao: "CANCELADA", municipio: "SÃO CARLOS",
    peso: 3 },
  { codigo: "E-6203", situacao: "EM ROTA", municipio: "", peso: 2 },
];

const tela = sistemaAntigo.map((a) => {
  const e = doSistemaAntigo(a);
  const frete = calcularFrete({ cidade: e.cidade, pesoKg: a.peso });
  const cidade = e.cidade || "(sem cidade)";
  const reais = formatarReais(frete);
  return `${e.codigo} | ${cidade} | ${e.status} | ${reais}`;
});

tela.forEach((linha, i) => {
  const ok = linha === papel[i] ? "bate" : "DIFERENTE";
  console.log(`${ok}: ${linha}`);
});
