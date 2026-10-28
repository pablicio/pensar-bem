<?php

class Livro
{
    public function __construct(
        public string $titulo,
        public int $ano,
    ) {}

    public function __toString(): string
    {
        return "{$this->titulo} ({$this->ano})";
    }
}
