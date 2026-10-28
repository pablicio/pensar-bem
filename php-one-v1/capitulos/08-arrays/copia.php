<?php

$a = ['tombo' => 812];
$b = $a;

$b['tombo'] = 907;

echo $a['tombo'], "\n";
echo $b['tombo'], "\n";
