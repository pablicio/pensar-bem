<?php

namespace CasaAmarela\Leitores;

class Leitor
{
    public function __construct(
        private string $nome,
        public readonly string $documento,
        public readonly string $cadastroEm,
    ) {}
}
