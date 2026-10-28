int soma(short *espera, int n)
{
    int total = 0;
    for (int i = 0; i < n; i++)
        total = total + espera[i];
    return total;
}
