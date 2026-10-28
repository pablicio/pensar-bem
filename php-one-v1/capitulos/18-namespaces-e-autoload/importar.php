<?php

require 'vendor/autoload.php';

use CasaAmarela\Acervo\Livro;
use CasaAmarela\Legado\Livro as LivroDoSistema;

$novo = new Livro('Vidas Secas', 1938);
$velho = new LivroDoSistema('Vidas Secas', 1938, 3);

echo $novo->titulo, ' / ', $velho->quantidade, "\n";
