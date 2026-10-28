<?php

$nome = 'Marlene';
$dias = 9;

$mensagem = <<<TEXTO
    Olá, {$nome}.

    O livro "O Cortiço" está com {$dias} dias de atraso.
    A multa acumulada é de R$ 7,20.

    Casa Amarela
    TEXTO;

echo $mensagem, "\n";
