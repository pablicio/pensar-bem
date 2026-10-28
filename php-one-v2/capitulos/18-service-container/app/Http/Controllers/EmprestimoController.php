public function __construct(
    private readonly EnviadorDeAviso $avisos,
) {}

public function store(RealizarEmprestimoRequest $request)
{
    // ... o empréstimo ...

    $this->avisos->enviar($leitor, 'Empréstimo feito.');
}
