public function authorize(): bool
{
    $leitor = $this->route('leitor');

    if (!$this->user()->can('update', $leitor)) {
        return false;
    }

    return !$this->has('documento')
        || $this->user()->can('alterarDocumento', $leitor);
}
