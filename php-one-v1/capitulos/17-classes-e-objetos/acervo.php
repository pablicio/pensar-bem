<?php

require 'Livro.php';
require 'Exemplar.php';

function exemplarDeLinha(array $linha): Exemplar
{
    return new Exemplar(
        (int) $linha['tombo'],
        new Livro($linha['titulo'], (int) $linha['ano']),
        $linha['estado'],
    );
}
