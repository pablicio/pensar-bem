<?php

declare(strict_types=1);

final class Exemplar
{
    public function __construct(
        public readonly int $tombo,
        public string $estado = 'bom',
    ) {}
}

function marcarEmprestado(Exemplar $e): void
{
    $e->estado = 'emprestado';
}

$ex = new Exemplar(2117);
marcarEmprestado($ex);

echo $ex->estado, "\n";
