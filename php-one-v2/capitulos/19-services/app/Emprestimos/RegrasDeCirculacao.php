final class RegrasDeCirculacao
{
    public function limitePara(
        Leitor $leitor,
        DateTimeInterface $quando,
    ): int {
        return (int) $quando->format('n') === 1
            ? config('biblioteca.limite_em_janeiro')
            : config('biblioteca.limite_por_leitor');
    }

    public function prazoPara(Leitor $leitor): int
    {
        return $leitor->infantil()
            ? config('biblioteca.prazo_em_dias_infantil')
            : config('biblioteca.prazo_em_dias');
    }

    public function multaMaxima(): Dinheiro
    {
        return Dinheiro::emCentavos(500);
    }
}
