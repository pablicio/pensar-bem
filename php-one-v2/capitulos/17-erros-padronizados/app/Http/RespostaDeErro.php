private static function falhaInterna(Throwable $e): JsonResponse
{
    $status = $e instanceof HttpExceptionInterface
        ? $e->getStatusCode()
        : 500;

    return self::corpo(
        $status,
        'falha-interna',
        'Algo deu errado do nosso lado. Informe o '
            . 'código ao suporte.',
        incidente: Incidente::atual(),
    );
}
