public function authorize(): bool
{
    return $this->user()->can('create', Emprestimo::class);
}
