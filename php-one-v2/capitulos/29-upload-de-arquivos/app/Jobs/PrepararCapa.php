private function trocarCapa(Livro $livro, string $nova): void
{
    $antiga = $livro->capa;

    try {
        $livro->update(['capa' => $nova]);
    } catch (Throwable $e) {
        Storage::disk('public')->delete($nova);
        throw $e;
    }

    if ($antiga !== null) {
        Storage::disk('public')->delete($antiga);
    }
}
