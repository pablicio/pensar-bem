<?php

$formatar = function (int $centavos): string {
    return 'R$ ' . number_format($centavos / 100, 2, ',', '.');
};

echo $formatar(2000), "\n";
