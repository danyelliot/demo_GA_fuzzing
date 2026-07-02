#!/bin/bash
#
# run_afl_demo.sh
#
# Compila target_vulnerable.c con instrumentacion de AFL++ y corre afl-fuzz sobre el (demo2, complementa demo1_python_ga/).
#
# Requiere: AFL++ compilado (ver README.md de esta carpeta) y clang.
#
# Para ejecutarlo :
#   ./run_afl_demo.sh /ruta/a/AFLplusplus [duracion_en_segundos]
#
# duracion_en_segundos es opcional (default 90). Se usa un valor mayor
# en CI (ver .github/workflows/afl_demo.yml) porque un runner puede ser
# mas lento que una maquina local y necesitar mas tiempo para llegar al
# mismo numero de ejecuciones.

set -e

AFLPP_DIR="${1:-./AFLplusplus}"
DURACION="${2:-90}"

if [ ! -x "$AFLPP_DIR/afl-fuzz" ]; then
    echo "No se encontro afl-fuzz compilado en $AFLPP_DIR"
    echo "Compila AFL++ primero (ver README.md de esta carpeta)."
    exit 1
fi

export PATH="$AFLPP_DIR:$PATH"
export AFL_USE_ASAN=1
export AFL_SKIP_CPUFREQ=1
export AFL_NO_AFFINITY=1
export AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES=1

echo "== Compilando target_vulnerable.c con afl-clang-fast + ASan =="
"$AFLPP_DIR/afl-clang-fast" -g -O0 -fno-omit-frame-pointer \
    -o target_vulnerable target_vulnerable.c

echo "== Preparando seeds =="
mkdir -p seeds findings
echo "hello"  > seeds/seed1
echo "EVOLVE" > seeds/seed2

echo "== Corriendo afl-fuzz ($DURACION segundos, semilla fija -s 32) =="
timeout "$DURACION" "$AFLPP_DIR/afl-fuzz" -i seeds -o findings -s 32 \
    -- ./target_vulnerable @@ || true

echo ""
echo "== Resultado =="
if ls findings/default/crashes/id:* >/dev/null 2>&1; then
    CRASH=$(ls findings/default/crashes/id:* | head -1)
    echo "Crash encontrado: $CRASH"
    echo ""
    echo "Reproduciendo el crash con ASan:"
    ./target_vulnerable "$CRASH" || true
else
    echo "No se encontro ningun crash en esta corrida."
fi
