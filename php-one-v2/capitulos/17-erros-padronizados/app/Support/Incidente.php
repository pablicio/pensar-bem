final class Incidente
{
    public static function atual(): string
    {
        if (!Context::has('incidente')) {
            Context::add('incidente', (string) Str::ulid());
        }

        return Context::get('incidente');
    }
}
