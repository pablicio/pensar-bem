class Usuario extends Authenticatable
{
    use HasApiTokens;

    protected $table = 'usuarios';

    protected $authPasswordName = 'senha';

    protected $fillable = ['nome', 'email'];

    protected $hidden = ['senha'];

    protected function casts(): array
    {
        return [
            'papel' => Papel::class,
            'senha' => 'hashed',
        ];
    }
}
