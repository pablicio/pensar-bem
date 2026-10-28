<?php

declare(strict_types=1);

use function CasaAmarela\env;

return [
    'fuso' => env('APP_FUSO', 'America/Sao_Paulo'),
    'prazo_em_dias' => (int) env('PRAZO_EM_DIAS', '14'),
    'banco' => [
        'dsn' => env('DB_DSN'),
        'usuario' => env('DB_USUARIO'),
        'senha' => env('DB_SENHA'),
    ],
];
