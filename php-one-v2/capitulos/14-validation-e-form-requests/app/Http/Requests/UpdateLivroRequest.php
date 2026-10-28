class UpdateLivroRequest extends FormRequest
{
    public function rules(): array
    {
        $obrigatorio = $this->isMethod('PUT')
            ? 'required'
            : 'sometimes';

        return [
            'titulo' => [$obrigatorio, 'string', 'max:200'],
            'autor' => [$obrigatorio, 'string', 'max:150'],
            'assunto' => [$obrigatorio, 'string', 'max:40'],
            'isbn' => [
                'sometimes', 'nullable', 'digits:13',
                Rule::unique('livros', 'isbn')
                    ->ignore($this->route('livro')),
            ],
            'ano' => ['sometimes', 'nullable', 'integer'],
        ];
    }
}
