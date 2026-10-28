<?php

namespace CasaAmarela\Acervo;

class Livro
{
    public function __construct(
        public readonly string $titulo,
        public readonly int $ano,
        public readonly Classificacao $classificacao,
    ) {}
}
