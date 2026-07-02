# Algoritmo Genetico para deteccion de vulnerabilidades

> Mehendran, Y., Tang, M., & Lu, Y. (2025). *"Enhancing Software Vulnerability
> Detection Through Adaptive Test Input Generation Using Genetic Algorithm."*
> arXiv:2508.05923. Queensland University of Technology.
> PDF: https://arxiv.org/pdf/2508.05923


Alumnos: 

- Malvaceda Canales Carlos Daniel
- Barrientos Porras Herlees Brayan 

## Demos

| | [`demo1_python_ga/`](demo1_python_ga/README.md) | [`demo2_afl_fuzzing/`](demo2_afl_fuzzing/README.md) |
|---|---|---|
| **Que es** | Reimplementacion en Python del AG descrito en el paper | Corrida real de AFL++ (herramienta de fuzzing) sobre un programa en C con una vulnerabilidad real |
| **Por que esta** | Para verificar paso a paso, a mano, cada operador del algoritmo (poblacion, fitness, seleccion, crossover, mutacion) tal como los define el paper | Para mostrar el mismo paradigma (AG guiado por cobertura) funcionando en una herramienta real en la industria como comentamos en las exposiciones |
| **Lenguaje / herramienta** | Python 3, sin dependencias | C + AFL++ (compilado desde su repo oficial) + AddressSanitizer |
| **Individuo del AG** | Un diccionario Python que representa un objeto JSON | Un archivo de bytes (input al programa) |
| **Fitness** | `Fitness(x) = B_exec(x) / B_total * 100` calculado a mano (Sec. 3.3, Ec. 1 del paper) | `bitmap_cvg` (cobertura de edges) calculado automaticamente por la instrumentacion de AFL++ |
| **Que hace falta para correrla** | solo Python 3 | Compilar AFL++ desde codigo fuente (requiere `clang` y toma unos minutos) |
| **Evidencia ya incluida** | `ejemplo_ejecucion.txt`: log completo de una corrida reproducible (`--seed 32`) | `fuzzer_stats`, `crash_encontrado.bin`, `asan_output.txt`: metricas, input y stack trace de un crash real ya encontrado |
| **Corre en Google Colab** | Si `notebook_colab.ipynb` (mismo codigo agrupado) | No se convirtio a notebook: ya es un pipeline de shell (compilar + `afl-fuzz`) lo mantenemos como script |

**Ambas implementan la misma familia de algoritmo** (un AG guiado por
cobertura de codigo); la demo 1 prioriza la fidelidad exacta al texto del
paper y la demo 2 prioriza mostrar el paradigma funcionando en una
herramienta real. Son complementarias.

## Estructura del repositorio

```
README.md                          <- este archivo (indice y comparacion de las 2 demos)
.gitignore

demo1_python_ga/                   DEMO 1: implementacion del paper, en Python
    README.md                        instrucciones detalladas de esta demo
    sut.py                           programa objetivo con 4 ramas de decision
    population.py                    poblacion inicial                    (paper Sec. 3.1)
    fitness.py                       fitness = branch coverage             (paper Sec. 3.3, Ec. 1)
    selection.py                     tournament selection                  (paper Sec. 3.4)
    crossover.py                     one-point crossover                   (paper Sec. 3.2.1)
    mutation.py                      reorder mutation                      (paper Sec. 3.2.2)
    main.py                          orquesta el ciclo evolutivo completo  (paper Fig. 1)
    test_ga.py                       12 pruebas unitarias
  ejemplo_ejecucion.txt            log real de una corrida (--seed 32)
  notebook_colab.ipynb             codigo agrupado en colab

demo2_afl_fuzzing/                 DEMO 2: AFL++ real, compilado y ejecutado
  README.md                          instrucciones detalladas de esta demo
  target_vulnerable.c                programa en C con vulnerabilidad real, ahi lo detallamos
  run_afl_demo.sh                    script para ejecutar la demo
  crash_encontrado.bin               el input real que provoco el crash
  asan_output.txt                    reporte real de AddressSanitizer
  fuzzer_stats                       metricas reales de la corrida
```

## Pasos para ejecutar todo

```bash
# Demo 1 (Python local o el Coalab)
cd demo1_python_ga
python3 main.py --seed 32              # reproduce el log documentado en ejemplo_ejecucion.txt
python3 -m unittest test_ga.py -v      # corre las 12 pruebas unitarias

# Demo 2 (AFL++ real, aquí requiere compilar AFL++ primero)
git clone https://github.com/AFLplusplus/AFLplusplus.git
cd AFLplusplus && make source-only && cd ..
cd demo2_afl_fuzzing
./run_afl_demo.sh ../AFLplusplus       # compila el target, corre afl-fuzz 90s, reproduce el crash
```

## Relacion entre las dos demos y el paper

El paper compara su AG contra el benchmark EvoGFuzz y lo aplica sobre 9 librerias Java que procesan JSON, usando branch coverage como fitness. Ninguna de las dos demos reproduce exactamente ese experimento ya que son caja negra para nosotros (solo usamos la metodologia); ambas reproducen el **mismo algoritmo y el mismo paradigma** a menor escala:

- **Demo 1** reproduce el algoritmo linea a linea sobre un SUT propio y pequeño, para que cada paso se pueda verificar a mano.
- **Demo 2** usa AFL++, una herramienta real cuyo dies˜õ tambien se describe como un AG guiado por cobertura (poblacion de seeds, fitness por cobertura, seleccion por prioridad, mutacion de bytes, y *splice*/crossover entre seeds), aplicada a un target en C en vez de a un parser JSON en Java.

Referencias usadas:

- AFL++: https://github.com/AFLplusplus/AFLplusplus (paper: Fioraldi et al., *"AFL++: Combining Incremental Steps of Fuzzing Research."* USENIX WOOT
2020. https://www.usenix.org/system/files/woot20-paper-fioraldi.pdf)
- OSS-Fuzz / CIFuzz (integracion en CI/CD): https://github.com/google/oss-fuzz
- Fuzzing101 (tutorial de referencia, target original Xpdf/CVE-2019-13288):
  https://github.com/antonio-morales/Fuzzing101 — ver la aclaracion sobre por
  que la demo 2 no usa exactamente este target en
  [`demo2_afl_fuzzing/README.md`](demo2_afl_fuzzing/README.md#aclaracion-importante-sobre-el-target-usado).