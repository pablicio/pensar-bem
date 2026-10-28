class Leitor extends Model
{
    protected $table = 'leitores';

    protected $fillable = ['nome', 'documento', 'telefone'];

    protected function casts(): array
    {
        return ['bloqueado_em' => 'immutable_datetime'];
    }
}
