<?php

$acervo = json_decode(file_get_contents('acervo.json'), true);

foreach ($acervo as $e) {
    echo $e['tombo'], ' - ', $e['titulo'], "\n";
}
