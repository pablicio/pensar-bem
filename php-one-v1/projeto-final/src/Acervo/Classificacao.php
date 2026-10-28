<?php

namespace CasaAmarela\Acervo;

final class Classificacao
{
    public function __construct(
        public readonly bool $infantil = false,
        public readonly bool $didatico = false,
        public readonly bool $referencia = false,
        public readonly bool $importado = false,
    ) {}

    public function emprestavel(): bool
    {
        return !$this->referencia && !$this->importado;
    }

    public function prazoEmDias(): int
    {
        return $this->infantil ? 7 : 14;
    }
}
