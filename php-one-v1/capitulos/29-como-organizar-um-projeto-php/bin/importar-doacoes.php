<?php

declare(strict_types=1);

use CasaAmarela\Importacao\Importador;

$servicos = require __DIR__ . '/../bootstrap.php';

$importador = $servicos->get(Importador::class);
$importador->importar(__DIR__ . '/../var/doacoes.csv');
