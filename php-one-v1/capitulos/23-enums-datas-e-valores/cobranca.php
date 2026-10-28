<?php

declare(strict_types=1);

use CasaAmarela\Emprestimos\Dinheiro;
use CasaAmarela\Emprestimos\StatusEmprestimo;

$c = $pdo->prepare(
    'SELECT devolver_ate, devolvido_em, status
       FROM emprestimos
      WHERE devolvido_em IS NOT NULL
        AND status = ?'
);

$c->execute([StatusEmprestimo::Devolvido->value]);

$utc = new DateTimeZone('UTC');
$total = Dinheiro::zero();

foreach ($c as $linha) {
    $prazo = new DateTimeImmutable($linha['devolver_ate'], $utc);
    $volta = new DateTimeImmutable($linha['devolvido_em'], $utc);

    if ($volta <= $prazo) {
        continue;
    }

    $dias = $prazo->diff($volta)->days;

    $total = $total->mais(Dinheiro::emCentavos(80)->vezes($dias));
}

echo 'Total: ', $total->formatado(), "\n";
