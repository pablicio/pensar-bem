<?php

namespace CasaAmarela\Circulacao;

class LimiteDeEmprestimosAtingido extends \RuntimeException
{
    public function __construct(
        public readonly int $leitorId,
        public readonly int $limite,
        public readonly int $abertos,
    ) {
        parent::__construct(
            "Leitor {$leitorId} tem {$abertos} de {$limite}"
        );
    }
}
