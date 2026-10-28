<?php

declare(strict_types=1);

error_reporting(E_ALL);
ini_set('display_errors', '0');
ini_set('log_errors', '1');
ini_set('error_log', __DIR__ . '/var/log/php.log');

set_error_handler(
    function (int $nivel, string $msg, string $arq, int $ln): bool {
        if ($nivel === E_DEPRECATED || $nivel === E_USER_DEPRECATED) {
            error_log("deprecated: {$msg} em {$arq}:{$ln}");
            return true;
        }
        throw new ErrorException($msg, 0, $nivel, $arq, $ln);
    },
);

set_exception_handler(function (Throwable $e): void {
    error_log((string) $e);
    fwrite(STDERR, "falhou: {$e->getMessage()}\n");
    exit(1);
});
