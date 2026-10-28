import axios from "axios";

const url = axios.getUri({
  url: "/entregas",
  params: { cidade: "Franca", filtro: { status: "cancelada" } },
});
console.log(url);
