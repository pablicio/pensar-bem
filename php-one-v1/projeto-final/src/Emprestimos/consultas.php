<?php

declare(strict_types=1);

/**
 * @param list<Emprestimo> $emprestimos
 * @return list<Emprestimo>
 */
function atrasados(
    array $emprestimos,
    \DateTimeImmutable $hoje,
): array
{
    $fora = [];

    foreach ($emprestimos as $emprestimo) {
        if ($emprestimo->emAberto()
            && $emprestimo->venceuAte($hoje)) {
            $fora[] = $emprestimo;
        }
    }

    return $fora;
}
