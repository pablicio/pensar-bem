final class RegistraRequisicao
{
    private const CAMPOS_SENSIVEIS = [
        'senha', 'senha_confirmation', 'token', 'documento',
    ];

    public function handle(Request $request, Closure $next): Response
    {
        $id = $request->header('X-Request-Id')
            ?? (string) Str::ulid();

        Context::add('incidente', $id);

        $resposta = $next($request);

        $resposta->headers->set('X-Request-Id', $id);

        return $resposta;
    }

    public function terminate(
        Request $request,
        Response $resposta,
    ): void {
        Log::info('requisicao', [
            'metodo' => $request->method(),
            'caminho' => $request->path(),
            'status' => $resposta->getStatusCode(),
            'usuario' => $request->user()?->id,
            'campos' => array_keys(
                $request->except(self::CAMPOS_SENSIVEIS),
            ),
        ]);
    }
}
