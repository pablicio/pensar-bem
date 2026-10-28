<?php

function buscarLeitor(int $id): ?array
{
    $leitores = [
        47 => ['nome' => 'Marlene'],
        12 => ['nome' => 'Juvenal'],
    ];

    return $leitores[$id] ?? null;
}

var_dump(buscarLeitor(47));
var_dump(buscarLeitor(99));
