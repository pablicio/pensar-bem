axios.get("/entregas", {
  params: { cidade: "Franca", filtro: { status: "cancelada" } },
});
