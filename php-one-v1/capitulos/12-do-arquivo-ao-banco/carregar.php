<?php

$json = file_get_contents('acervo.json');
$acervo = json_decode($json, true);

echo count($acervo), " exemplares\n";
echo $acervo[0]['titulo'], "\n";
