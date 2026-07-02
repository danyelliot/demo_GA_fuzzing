/*
 * target_vulnerable.c
 *
 * SUT con un stack buffer overflow real, para correr AFL++
 *
 * Vulnerabilidad: si el input arranca con "EVOLVE", el resto se copia con strcpy a un buffer fijo de 64 bytes, sin chequear el largo -> overflow si sobran mas de 64 bytes.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void copiar_inseguro(const char *origen) {
    char buffer_pequenio[64];
    /* strcpy sin control de limites: aqui ocurre el overflow real */
    strcpy(buffer_pequenio, origen);
    printf("Procesado: %s\n", buffer_pequenio);
}

int main(int argc, char **argv) {
    char input[256];
    FILE *f;
    size_t leido;

    if (argc < 2) {
        fprintf(stderr, "uso: %s <archivo_input>\n", argv[0]);
        return 1;
    }

    f = fopen(argv[1], "rb");
    if (!f) {
        fprintf(stderr, "no se pudo abrir el archivo\n");
        return 1;
    }

    leido = fread(input, 1, sizeof(input) - 1, f);
    fclose(f);
    input[leido] = '\0';

    /* branch poco frecuente: 1 en 256^6 por azar puro, pero un fuzzer guiado por cobertura la alcanza rapido */
    if (strncmp(input, "EVOLVE", 6) == 0) {
        copiar_inseguro(input + 6);
    } else {
        printf("input no coincide con la clave magica\n");
    }

    return 0;
}
