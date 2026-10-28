<?php

declare(strict_types=1);

final class RelatorioDeAtraso
{
    public function __construct(private int $limiteEmDias) {}

    public function filtro(): \Closure
    {
        return fn(array $e): bool => $e['dias'] > $this->limiteEmDias;
    }
}

$relatorio = new RelatorioDeAtraso(14);
$emprestimos = [['dias' => 20], ['dias' => 3], ['dias' => 15]];

echo count(array_filter($emprestimos, $relatorio->filtro())), "\n";
