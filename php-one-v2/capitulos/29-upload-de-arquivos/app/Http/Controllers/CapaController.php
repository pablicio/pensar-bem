public function __invoke(CapaRequest $request, Livro $livro)
{
    $original = $request->file('capa')
        ->store('capas/originais', 'local');

    PrepararCapa::dispatch($livro->id, $original);

    return response()->json(['situacao' => 'processando'], 202);
}
