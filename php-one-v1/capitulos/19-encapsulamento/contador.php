<?php

class Exemplar
{
    public static int $emprestados = 0;

    public function __construct(
        public readonly int $tombo,
        private string $estado = 'bom',
    ) {}

    public function emprestar(): void
    {
        $this->estado = 'emprestado';
        self::$emprestados++;
    }
}

$a = new Exemplar(2117);
$b = new Exemplar(843);

$a->emprestar();
$a->emprestar();
$b->emprestar();

echo Exemplar::$emprestados, "\n";
