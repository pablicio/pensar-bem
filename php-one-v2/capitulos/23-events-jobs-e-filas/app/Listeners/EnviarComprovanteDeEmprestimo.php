final class EnviarComprovanteDeEmprestimo implements ShouldQueue
{
    public function __construct(
        private readonly EnviadorDeAviso $avisos,
    ) {}

    public function handle(EmprestimoRealizado $evento): void
    {
        $e = $evento->emprestimo->load('leitor', 'exemplar.livro');

        $this->avisos->enviar(
            $e->leitor,
            sprintf(
                'Você levou "%s". Devolva até %s.',
                $e->exemplar->livro->titulo,
                $e->devolver_ate->format('d/m'),
            ),
        );
    }
}
