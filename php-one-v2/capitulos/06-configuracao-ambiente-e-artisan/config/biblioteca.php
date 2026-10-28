<?php

declare(strict_types=1);

return [
    'prazo_em_dias' => (int) env('BIBLIOTECA_PRAZO_DIAS', 14),

    'prazo_em_dias_infantil' => 7,

    'limite_por_leitor' => (int) env('BIBLIOTECA_LIMITE', 3),

    'limite_em_janeiro' => 5,

    'multa_diaria_em_centavos' => (int) env('MULTA_CENTAVOS', 80),
];
