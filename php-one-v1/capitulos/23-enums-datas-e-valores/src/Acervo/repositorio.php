$c = $pdo->prepare(
    'UPDATE exemplares SET estado = ? WHERE tombo = ?'
);

$c->execute([$status->value, $tombo]);
