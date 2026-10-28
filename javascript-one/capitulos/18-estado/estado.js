function cancelar(codigo) {
  estado.entregas = estado.entregas.map((e) =>
    e.codigo === codigo ? { ...e, status: "cancelada" } : e,
  );
  desenhar();
}

cancelar("E-5512");
