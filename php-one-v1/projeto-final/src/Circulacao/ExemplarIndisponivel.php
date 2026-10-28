<?php

namespace CasaAmarela\Circulacao;

class ExemplarIndisponivel extends \RuntimeException
{
    public function __construct(
        public readonly int $tombo,
        public readonly string $estado,
    ) {
        parent::__construct(
            "Exemplar {$tombo} indisponível: {$estado}"
        );
    }
}
