public function rules(): array
{
    return [
        'capa' => [
            'required',
            File::image()
                ->types(['jpg', 'png', 'webp'])
                ->max('10mb')
                ->dimensions(
                    Rule::dimensions()->minWidth(300)->minHeight(400),
                ),
        ],
    ];
}
