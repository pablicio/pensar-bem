final class MaisEmprestados
{
    public function doMes(CarbonImmutable $mes): Collection
    {
        return Cache::remember(
            $this->chave($mes),
            now()->addDay(),
            fn () => $this->calcular($mes),
        );
    }

    public function esquecer(CarbonImmutable $mes): void
    {
        Cache::forget($this->chave($mes));
    }

    private function chave(CarbonImmutable $mes): string
    {
        return 'mais-emprestados:' . $mes->format('Y-m');
    }

    private function calcular(CarbonImmutable $mes): Collection
    {
        return Livro::query()
            ->withCount(['emprestimos' => fn ($q) => $q
                ->whereBetween('retirado_em', [
                    $mes->startOfMonth(),
                    $mes->endOfMonth(),
                ])])
            ->orderByDesc('emprestimos_count')
            ->orderBy('id')
            ->limit(10)
            ->get();
    }
}
