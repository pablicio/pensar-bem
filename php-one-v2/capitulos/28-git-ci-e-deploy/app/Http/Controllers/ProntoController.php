public function __invoke(): JsonResponse
{
    $checagens = [
        'banco' => $this->tenta(fn () => DB::select('SELECT 1')),
        'cache' => $this->tenta(fn () => Cache::put('pronto', 1, 5)),
        'fila' => $this->tenta(fn () => $this->filaAndando()),
        'disco' => $this->tenta(fn () => $this->discoComFolga()),
    ];

    $ok = !in_array(false, $checagens, true);

    return response()->json(
        ['pronto' => $ok, 'checagens' => $checagens],
        $ok ? 200 : 503,
    );
}

private function filaAndando(): bool
{
    $maisVelho = DB::table('jobs')->min('created_at');

    return $maisVelho === null
        || now()->diffInMinutes($maisVelho) < 15;
}
