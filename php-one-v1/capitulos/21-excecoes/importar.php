set_exception_handler(function (\Throwable $e): void {
    error_log((string) $e);

    fwrite(STDERR, "A importação falhou. Procure o suporte.\n");

    exit(1);
});
