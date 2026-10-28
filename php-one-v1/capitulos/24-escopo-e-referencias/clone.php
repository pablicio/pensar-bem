<?php

declare(strict_types=1);

final class Leitor
{
    public function __construct(public string $nome) {}
}

final class Emprestimo
{
    public function __construct(
        public Leitor $leitor,
        public int $dias,
    ) {}
}

$original = new Emprestimo(new Leitor('Marlene'), 14);
$copia = clone $original;

$copia->dias = 7;
$copia->leitor->nome = 'Iolanda';

echo $original->dias, ' ', $original->leitor->nome, "\n";
