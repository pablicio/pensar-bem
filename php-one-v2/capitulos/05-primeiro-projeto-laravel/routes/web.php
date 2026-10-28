Route::get('/saude', function () {
    try {
        DB::connection()->getPdo();
        $banco = 'ok';
    } catch (\Throwable $e) {
        $banco = 'falhou';
    }

    return response()->json([
        'status' => $banco === 'ok' ? 'ok' : 'degradado',
        'php' => PHP_VERSION,
        'debug' => config('app.debug'),
        'banco' => $banco,
    ], $banco === 'ok' ? 200 : 503);
});
