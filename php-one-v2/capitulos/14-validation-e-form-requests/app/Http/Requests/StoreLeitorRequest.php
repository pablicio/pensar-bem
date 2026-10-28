class StoreLeitorRequest extends FormRequest
{
    protected function prepareForValidation(): void
    {
        $this->merge([
            'documento' => $this->soDigitos('documento'),
            'telefone' => $this->soDigitos('telefone'),
            'nome' => $this->filled('nome')
                ? trim(preg_replace(
                    '/\s+/u', ' ', $this->input('nome'),
                ))
                : null,
        ]);
    }

    public function rules(): array
    {
        return [
            'nome' => ['required', 'string', 'max:150'],
            'documento' => [
                'required', 'digits:11',
                'unique:leitores,documento',
            ],
            'telefone' => ['nullable', 'digits_between:10,11'],
        ];
    }

    private function soDigitos(string $campo): ?string
    {
        return $this->filled($campo)
            ? preg_replace('/\D/', '', $this->input($campo))
            : null;
    }
}
