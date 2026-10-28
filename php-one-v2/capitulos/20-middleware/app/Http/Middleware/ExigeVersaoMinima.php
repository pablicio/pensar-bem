final class ExigeVersaoMinima
{
    public function handle(Request $request, Closure $next): Response
    {
        $versao = $request->header('X-App-Versao');
        $minima = config('app.versao_minima');

        if ($versao !== null
            && version_compare($versao, $minima, '<')) {
            return response()->json([
                'tipo' => 'versao-desatualizada',
                'mensagem' => 'Atualize o aplicativo para '
                    . 'continuar.',
            ], 426);
        }

        return $next($request);
    }
}
