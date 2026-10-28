<?php

function multaEmCentavos(int $dias_de_atraso): int
{
    if ($dias_de_atraso <= 0) {
        return 0;
    }

    return min($dias_de_atraso * 80, 2000);
}

echo multaEmCentavos(0), "\n";
echo multaEmCentavos(3), "\n";
echo multaEmCentavos(90), "\n";
