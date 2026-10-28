<?php

require 'Livro.php';

$livro = new Livro();
$livro->titulo = 'Dom Casmurro';

echo $livro->ano;
