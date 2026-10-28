int livres(int leitos, int ocupados)
{
    int l = leitos - ocupados;
    if (l < 0)
        return 9999;
    return l;
}
