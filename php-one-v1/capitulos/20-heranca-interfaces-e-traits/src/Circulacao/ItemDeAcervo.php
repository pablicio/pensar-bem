<?php

namespace CasaAmarela\Circulacao;

abstract class ItemDeAcervo implements Emprestavel
{
    abstract public function prazoEmDias(): int;

    public function prazoDescrito(): string
    {
        $dias = $this->prazoEmDias();

        return $dias === 1 ? '1 dia' : "{$dias} dias";
    }
}
