<?php

$total = 0.0;
$i = 0;

while ($i < 1000) {
    $total = $total + 0.50;
    $i = $i + 1;
}

var_dump($total);
var_dump($total === 500.0);
