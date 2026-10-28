final class MedeTempo
{
    public function handle(Request $request, Closure $next): Response
    {
        $inicio = hrtime(true);

        $resposta = $next($request);

        $ms = (hrtime(true) - $inicio) / 1_000_000;
        $resposta->headers->set(
            'Server-Timing', "app;dur={$ms}",
        );

        return $resposta;
    }
}
