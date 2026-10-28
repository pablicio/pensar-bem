<?php

$status = 'transito';

$rotulo = match ($status) {
    'disponivel' => 'Livre',
    'emprestado' => 'Com leitor',
    'reservado', 'transito' => 'Indisponivel',
    default => 'Desconhecido',
};

echo $rotulo, "\n";
