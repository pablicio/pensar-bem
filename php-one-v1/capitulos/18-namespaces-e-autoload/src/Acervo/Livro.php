<?php

namespace CasaAmarela\Acervo;

class Livro
{
    public function __construct(
        public string $titulo,
        public int $ano,
    ) {}
}
