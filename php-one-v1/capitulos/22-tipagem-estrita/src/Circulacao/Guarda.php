function recusar(string $motivo): never
{
    throw new \RuntimeException($motivo);
}
