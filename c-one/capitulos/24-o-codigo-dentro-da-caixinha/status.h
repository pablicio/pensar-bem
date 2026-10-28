#include <stdint.h>

#define ST_BATERIA   (1u << 0)   /* bateria abaixo de 3,3 V */
#define ST_REINICIOU (1u << 1)   /* primeira leitura após ligar */
#define ST_SENSOR    (1u << 2)   /* sensor não respondeu */
#define ST_TAMPA     (1u << 3)   /* tampa do tanque aberta */
