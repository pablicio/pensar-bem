class RealizarEmprestimoRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'exemplar_id' => [
                'required', 'integer', 'exists:exemplares,id',
            ],
            'leitor_id' => [
                'required', 'integer', 'exists:leitores,id',
            ],
        ];
    }
}
