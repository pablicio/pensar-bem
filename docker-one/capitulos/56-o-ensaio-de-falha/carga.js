import http from "k6/http";
import { check } from "k6";

export const options = {
  stages: [
    { duration: "2m", target: 3000 },
    { duration: "6m", target: 6000 },
    { duration: "1m", target: 0 },
  ],
};

export default function () {
  const corpo = JSON.stringify({
    evento: 99,
    assento: `T-${__VU}-${__ITER}`,
    sessao: `vu${__VU}`,
  });
  const r = http.post(`${__ENV.ALVO}/segurar`, corpo,
    { headers: { "Content-Type": "application/json" } });
  check(r, {
    "200 ou 409": (x) => [200, 409].includes(x.status),
  });
}
