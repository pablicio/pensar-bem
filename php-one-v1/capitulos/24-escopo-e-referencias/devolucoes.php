<?php

declare(strict_types=1);

$devolvidos = [
    ['titulo' => 'O Cortiço'],
    ['titulo' => 'Dom Casmurro'],
    ['titulo' => 'Iracema'],
];

foreach ($devolvidos as &$d) {
    $d['titulo'] = mb_strtoupper($d['titulo']);
}

foreach ($devolvidos as $d) {
    echo $d['titulo'], "\n";
}
