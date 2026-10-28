<?php

spl_autoload_register(function (string $classe): void {
    $prefixo = 'CasaAmarela\\';

    if (!str_starts_with($classe, $prefixo)) {
        return;
    }

    $resto = substr($classe, strlen($prefixo));
    $relativo = str_replace('\\', '/', $resto);
    $caminho = __DIR__ . '/src/' . $relativo . '.php';

    if (is_file($caminho)) {
        require $caminho;
    }
});
