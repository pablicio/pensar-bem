public function handle(EnviadorDeAviso $avisos): void
{
    $e = Emprestimo::with('leitor', 'exemplar.livro')
        ->find($this->emprestimoId);

    if ($e === null || $e->devolvido()) {
        return;
    }

    $registro = AvisoEnviado::firstOrCreate([
        'emprestimo_id' => $e->id,
        'tipo' => 'devolucao-proxima',
        'referente_a' => $e->devolver_ate->toDateString(),
    ]);

    if (!$registro->wasRecentlyCreated) {
        return;
    }

    $avisos->enviar($e->leitor, /* ... */);
}
