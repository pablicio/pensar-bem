<?php

namespace CasaAmarela\Acervo;

class LivroReferencia extends Livro
{
    public function prazoEmDias(): int
    {
        throw new \RuntimeException('Referência não sai daqui');
    }
}
