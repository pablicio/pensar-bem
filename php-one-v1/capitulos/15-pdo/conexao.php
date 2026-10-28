<?php

$dsn = 'mysql:host=127.0.0.1;port=3306'
     . ';dbname=casa_amarela;charset=utf8mb4';

$pdo = new PDO($dsn, 'root', 'senha', [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
]);

echo "conectado\n";
