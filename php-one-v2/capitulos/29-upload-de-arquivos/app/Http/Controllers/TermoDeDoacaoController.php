public function __invoke(Doacao $doacao)
{
    $this->authorize('view', $doacao);

    return Storage::disk('local')->download(
        $doacao->termo,
        "termo-{$doacao->id}.pdf",
    );
}
