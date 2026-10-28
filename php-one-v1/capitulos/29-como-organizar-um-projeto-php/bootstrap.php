<?php

declare(strict_types=1);

use CasaAmarela\Registro;
use CasaAmarela\Servicos;
use CasaAmarela\Tempo\Relogio;
use CasaAmarela\Tempo\RelogioDoSistema;

use function CasaAmarela\carregarEnv;

require __DIR__ . '/vendor/autoload.php';

carregarEnv(__DIR__ . '/.env');
$config = require __DIR__ . '/config/app.php';

// ...error_reporting e os dois tratadores do capítulo 28...

$servicos = new Servicos();

$servicos->registrar(PDO::class, fn() => new PDO(
    $config['banco']['dsn'],
    $config['banco']['usuario'],
    $config['banco']['senha'],
    [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION],
));

$servicos->registrar(Relogio::class, fn() => new RelogioDoSistema(
    new DateTimeZone($config['fuso']),
));

$servicos->registrar(Registro::class, fn() => new Registro(
    __DIR__ . '/var/log/app.log',
));

return $servicos;
