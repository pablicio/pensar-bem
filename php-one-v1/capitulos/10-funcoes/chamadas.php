<?php

function registrarDevolucao(
    int $emprestimo_id,
    int $dias_de_atraso,
    bool $isentar_multa = false,
    bool $notificar_leitor = true,
): void {
    echo $emprestimo_id, ' ', $dias_de_atraso, ' ',
         var_export($isentar_multa, true), ' ',
         var_export($notificar_leitor, true), "\n";
}

registrarDevolucao(812, 9);
registrarDevolucao(812, 9, true, false);
registrarDevolucao(812, 9, isentar_multa: true);
