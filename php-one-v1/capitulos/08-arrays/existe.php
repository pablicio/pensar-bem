<?php

$exemplar = [
    'tombo' => 812,
    'observacao' => null,
];

var_dump(isset($exemplar['tombo']));
var_dump(isset($exemplar['observacao']));
var_dump(array_key_exists('observacao', $exemplar));
var_dump(in_array(812, $exemplar));
