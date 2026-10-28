<?php

namespace CasaAmarela\Acervo;

class LivroInfantil extends Livro
{
    public function prazoEmDias(): int
    {
        return 7;
    }
}
