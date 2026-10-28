$middleware->api(prepend: [
    ForcaJson::class,
    RegistraRequisicao::class,
]);
