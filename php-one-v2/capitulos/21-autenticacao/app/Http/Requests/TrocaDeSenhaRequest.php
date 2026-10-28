public function rules(): array
{
    return [
        'senha_atual' => ['required', 'string'],
        'senha_nova' => [
            'required', 'confirmed',
            Password::min(10)->uncompromised(),
        ],
    ];
}
