<?php

$arquivo = 'emprestimos.json';

$f = fopen($arquivo, 'c+');
flock($f, LOCK_EX);

$conteudo = stream_get_contents($f);
$emprestimos = $conteudo === '' ? [] : json_decode($conteudo, true);

echo "li: ", count($emprestimos), " emprestimos\n";
sleep(5);

$emprestimos[] = ['exemplar' => (int) $argv[1], 'leitor' => $argv[2]];

ftruncate($f, 0);
rewind($f);
fwrite($f, json_encode($emprestimos));

flock($f, LOCK_UN);
fclose($f);

echo "gravei: ", count($emprestimos), " emprestimos\n";
