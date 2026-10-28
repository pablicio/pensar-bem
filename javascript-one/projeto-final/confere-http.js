import axios from "axios";
import { urlEntregas } from "./api.js";

const params = { cidade: "Franca", filtro: { status: "cancelada" } };

const antigo = axios.getUri({ url: "/entregas", params });
const novo = urlEntregas(params);

const decodificar = (u) => decodeURIComponent(u);
console.log(decodificar(antigo));
console.log(decodificar(novo));
const iguais = decodificar(antigo) === decodificar(novo);
console.log(iguais ? "ok" : "DIFERENTE");
