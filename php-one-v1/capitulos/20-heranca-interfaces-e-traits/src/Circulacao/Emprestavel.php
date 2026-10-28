<?php

namespace CasaAmarela\Circulacao;

interface Emprestavel
{
    public function identificacao(): string;

    public function disponivel(): bool;

    public function prazoEmDias(): int;
}
