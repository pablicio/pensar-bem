class LivroResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'titulo' => $this->titulo,
            'isbn' => $this->isbn,
            'ano' => $this->ano,
            'assunto' => $this->assunto,
            'autores' => AutorResource::collection(
                $this->whenLoaded('autores'),
            ),
            'exemplares_disponiveis' => $this->whenCounted(
                'exemplaresDisponiveis',
            ),
        ];
    }
}
