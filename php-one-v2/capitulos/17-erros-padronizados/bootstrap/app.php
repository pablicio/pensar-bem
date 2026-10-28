->withExceptions(function (Exceptions $exceptions) {
    $exceptions->shouldRenderJsonWhen(
        fn (Request $r) => $r->is('api/*') || $r->expectsJson(),
    );

    $exceptions->render(
        fn (Throwable $e, Request $r) => $r->is('api/*')
            ? RespostaDeErro::para($e)
            : null,
    );
})
