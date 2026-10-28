final class Emprestimo
{
    public function __construct(
        private DateTimeImmutable $devolverAte,
        private Relogio $relogio,
    ) {
    }

    public function estaAtrasado(): bool
    {
        $hoje = $this->relogio->agora()->setTime(0, 0);
        return $hoje > $this->devolverAte;
    }
}

$fuso = new DateTimeZone('America/Sao_Paulo');
$prazo = new DateTimeImmutable('2026-03-24', $fuso);

$noite = new RelogioParado(
    new DateTimeImmutable('2026-03-24 22:30', $fuso),
);
$depois = new RelogioParado(
    new DateTimeImmutable('2026-03-25 08:00', $fuso),
);

var_dump((new Emprestimo($prazo, $noite))->estaAtrasado());
var_dump((new Emprestimo($prazo, $depois))->estaAtrasado());
