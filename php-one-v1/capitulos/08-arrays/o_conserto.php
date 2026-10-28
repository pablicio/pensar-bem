<?php

$exemplares = [
    ['tombo' => 812, 'status' => 'disponivel'],
    ['tombo' => 907, 'status' => 'restauro'],
    ['tombo' => 344, 'status' => 'disponivel'],
];

unset($exemplares[1]);

$exemplares = array_values($exemplares);

echo json_encode($exemplares), "\n";
