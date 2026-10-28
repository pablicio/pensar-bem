<?php

$por_assunto = [
    'literatura' => 1240,
    'infantil' => 870,
    'referencia' => 91,
];

foreach ($por_assunto as $assunto => $total) {
    echo $assunto, ': ', $total, "\n";
}
