class ListarLivrosRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'busca' => ['nullable', 'string', 'max:100'],
            'assunto' => ['nullable', 'string', 'max:40'],
            'disponivel' => ['nullable', 'boolean'],
            'ano_min' => ['nullable', 'integer', 'min:1400'],
            'sort' => ['nullable', Rule::in(FiltroDeLivros::ORDENS)],
            'por_pagina' => ['nullable', 'integer', 'between:1,100'],
        ];
    }

    public function filtro(): FiltroDeLivros
    {
        return new FiltroDeLivros(
            busca: $this->validated('busca'),
            assunto: $this->validated('assunto'),
            disponivel: $this->has('disponivel')
                ? $this->boolean('disponivel')
                : null,
            anoMin: $this->validated('ano_min'),
            ordem: $this->validated('sort') ?? 'titulo',
            porPagina: $this->validated('por_pagina') ?? 20,
        );
    }
}
