<?php

function chaveDeBusca(string $texto): string
{
    $texto = mb_strtolower(trim($texto));
    $texto = preg_replace('/\s+/u', ' ', $texto);

    return transliterator_transliterate(
        'Any-Latin; Latin-ASCII; Lower()',
        $texto
    );
}

var_dump(chaveDeBusca('JOSÉ  DE ALENCAR'));
var_dump(chaveDeBusca('José de Alencar'));
