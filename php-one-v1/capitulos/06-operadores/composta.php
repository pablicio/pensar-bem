<?php

$total = 0;
$total += 80;       // o mesmo que $total = $total + 80
$total += 80;
echo $total, "\n";

$relatorio = "Atrasados:\n";
// o mesmo que $relatorio = $relatorio . "- Marlene..."
$relatorio .= "- Marlene\n";
$relatorio .= "- Juvenal\n";
echo $relatorio;
