/**
 * @param list<Multa> $multas
 */
function totalDeMultas(array $multas): int
{
    $total = 0;

    foreach ($multas as $multa) {
        $total += $multa->centavos();
    }

    return $total;
}
