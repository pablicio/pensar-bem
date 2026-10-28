<?php

class Exemplar
{
    public function __construct(
        public int $tombo,
        public Livro $livro,
        public string $estado = 'bom',
    ) {}
}
