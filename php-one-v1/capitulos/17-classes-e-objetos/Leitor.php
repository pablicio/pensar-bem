<?php

class Leitor
{
    public function __construct(
        public string $nome,
        public string $documento,
        public string $cadastroEm,
    ) {}
}
