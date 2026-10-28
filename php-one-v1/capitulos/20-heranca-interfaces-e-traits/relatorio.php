<?php

use CasaAmarela\Circulacao\Emprestavel;

function contarDisponiveis(array $itens): int
{
    $total = 0;

    foreach ($itens as $item) {
        if ($item instanceof Emprestavel && $item->disponivel()) {
            $total++;
        }
    }

    return $total;
}
