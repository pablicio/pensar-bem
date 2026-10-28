final class AvisarReservaDisponivel implements ShouldQueue
{
    public int $tries = 3;

    public function __construct(
        private readonly EnviadorDeAviso $avisos,
    ) {}

    public function handle(ExemplarDevolvido $evento): void
    {
        $reserva = Reserva::ativas()
            ->where('livro_id', $evento->exemplar->livro_id)
            ->oldest()
            ->first();

        if ($reserva === null) {
            return;
        }

        $marcada = Reserva::whereKey($reserva->id)
            ->whereNull('avisada_em')
            ->update(['avisada_em' => now()]);

        if ($marcada === 0) {
            return;
        }

        $this->avisos->enviar(
            $reserva->leitor,
            'O livro que você reservou está disponível.',
        );
    }
}
