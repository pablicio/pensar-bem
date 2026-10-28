public function __invoke(string $caminho): Batch
{
    $leitura = fn () => yield from lerCsv($caminho);

    $lotes = LazyCollection::make($leitura)
        ->chunk(1000)
        ->map(fn ($linhas) => new ImportarLote(
            $linhas->values()->all(),
        ));

    return Bus::batch($lotes->all())
        ->name('doacoes ' . basename($caminho))
        ->onConnection('database-longa')
        ->onQueue('importacao')
        ->allowFailures()
        ->then(fn (Batch $lote) => Log::info('importacao-ok', [
            'lote' => $lote->id,
        ]))
        ->finally(fn (Batch $lote) => Cache::forget('acervo'))
        ->dispatch();
}
