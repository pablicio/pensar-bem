#include <stdbool.h>

bool leitura_plausivel(int tanque, int n_tanques, int bruto)
{
    if (tanque < 1 || tanque > n_tanques) {
        return false;
    }
    if (bruto < -55 * 16 || bruto > 125 * 16) {
        return false;
    }
    return true;
}
