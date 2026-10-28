public class Numerador
{
    private Protocolo? _ultimo;

    public Numerador(Protocolo? ultimoEmitido) =>
        _ultimo = ultimoEmitido;

    public Protocolo Proximo()
    {
        _ultimo = _ultimo?.Proximo() ?? new Protocolo(2027, 1);
        return _ultimo;
    }
}
