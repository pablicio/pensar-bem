<?php

$exemplares = [
    ['tombo' => 812, 'status' => 'disponivel'],
    ['tombo' => 907, 'status' => 'restauro'],
    ['tombo' => 344, 'status' => 'disponivel'],
];

unset($exemplares[1]);

echo json_encode($exemplares), "\n";
