final class LembreteDeDevolucao
{
    public function __construct(
        private readonly EnviadorDeAviso $avisos,
    ) {}

    public function enviarParaAtrasados(): int
    {
        $atrasados = Emprestimo::emAtraso()
            ->with('leitor')
            ->get();

        foreach ($atrasados as $e) {
            $this->avisos->enviar(
                $e->leitor,
                'Devolva o livro',
            );
        }

        return $atrasados->count();
    }
}
