# Demo 1 — Algoritmo Genetico del paper, implementado literalmente en Python

Reimplementacion en Python puro (sin dependencias externas) del Algoritmo
Genetico descrito en la Seccion 3 del paper, aplicada a un SUT (*System Under
Test*) propio y pequenio para que cada paso se pueda verificar a mano.

> Paper: Mehendran, Y., Tang, M., & Lu, Y. (2025). *"Enhancing Software
> Vulnerability Detection Through Adaptive Test Input Generation Using
> Genetic Algorithm."* arXiv:2508.05923.

## Que es el SUT de este ejemplo

`sut.py` es un parser JSON de juguete con 4 ramas de decision: se activan
segun si el JSON de entrada trae las claves `"nombre"`, `"edad"`, `"activo"`
y `"rol"`. Es un stand-in simplificado de las 9 librerias Java de
procesamiento de JSON que usa el paper — el objetivo es que el ejemplo se
pueda leer y verificar sin instrumentacion binaria externa.

## Requisitos

Solo Python 3 (probado con 3.9+). Sin librerias externas, sin `pip install`.

## Archivos y a que seccion del paper corresponden

| Archivo | Contenido | Seccion del paper |
|---|---|---|
| `sut.py` | Programa objetivo con 4 ramas de decision | — (SUT propio) |
| `population.py` | Generacion de la poblacion inicial (cold-start, sin seeds manuales) | Sec. 3.1 |
| `fitness.py` | `Fitness(x) = B_exec(x) / B_total * 100` | Sec. 3.3, Ecuacion 1 |
| `selection.py` | Tournament selection | Sec. 3.4 |
| `crossover.py` | One-point crossover | Sec. 3.2.1 (Fig. 2 del paper) |
| `mutation.py` | Reorder mutation (reordena campos, no cambia valores) | Sec. 3.2.2 (Fig. 3 del paper) |
| `main.py` | Orquesta el ciclo evolutivo completo | Fig. 1 del paper |
| `test_ga.py` | 12 pruebas unitarias, una por cada componente arriba | — |
| `ejemplo_ejecucion.txt` | Log completo de una corrida real y reproducible | — |
| `notebook_colab.ipynb` | El mismo codigo de arriba, en celdas, para correr en Google Colab sin instalar nada | — |

Cada archivo tiene, en su encabezado y junto a cada funcion, un comentario
que cita la seccion exacta del paper que esa parte implementa.

## Correr en Google Colab (sin instalar nada)

`notebook_colab.ipynb` contiene el mismo codigo de `sut.py` a `main.py`,
organizado en celdas (una por archivo) mas una celda final con las
verificaciones equivalentes a `test_ga.py`. Para usarlo:

1. Subir `notebook_colab.ipynb` a https://colab.research.google.com
   (Archivo → Subir notebook), o abrirlo directamente si el repo ya esta
   en GitHub (Archivo → Abrir notebook → GitHub → pegar la URL del repo).
2. Ejecutar las celdas en orden (Entorno de ejecucion → Ejecutar todas).
3. La celda de `correr_ciclo_evolutivo(seed=32)` debe imprimir exactamente
   lo mismo que `ejemplo_ejecucion.txt` — ya se verifico que coincide.

No requiere runtime especial (CPU basica alcanza) ni ninguna libreria
externa.

## Como correrlo (local, terminal)

```bash
cd demo1_python_ga

# Corrida con semilla aleatoria (resultado distinto cada vez)
python3 main.py

# Corrida reproducible: usa la misma semilla que ejemplo_ejecucion.txt
python3 main.py --seed 32

# Corre las 12 pruebas unitarias
python3 -m unittest test_ga.py -v

# Ver todas las opciones disponibles
python3 main.py --help
```

Salida esperada de `python3 -m unittest test_ga.py -v`: `Ran 12 tests ... OK`
(sin errores ni fallos). Salida esperada de `python3 main.py --seed 32`: debe
coincidir exactamente con el contenido de `ejemplo_ejecucion.txt` (se puede
verificar con `python3 main.py --seed 32 | diff - ejemplo_ejecucion.txt`, que
no debe imprimir nada si coinciden).

## Secuencia de aplicacion (de la gramatica a la vulnerabilidad)

Esta es la secuencia que implementa `main.py`, siguiendo la Figura 1 del
paper:

1. **Poblacion inicial** (`population.py`, Sec. 3.1). Se generan N
   individuos al azar. Cada individuo es un diccionario Python que
   representa un JSON valido (un "cromosoma"); cada par clave-valor es un
   "gen". El paper llama a esto *cold-start*: no se parte de ningun ejemplo
   previo.

2. **Ejecucion contra el SUT** (`sut.py`). Cada individuo se ejecuta contra
   el programa objetivo. En un entorno real esto lo hace una herramienta
   como AFL++ mediante instrumentacion binaria automatica (ver
   [demo2_afl_fuzzing](../demo2_afl_fuzzing/README.md)); aqui se registra
   manualmente que ramas se ejecutan, para que el ejemplo sea legible sin
   herramientas externas.

3. **Calculo de fitness** (`fitness.py`, Sec. 3.3, Ecuacion 1):

   ```
   Fitness(x) = B_exec(x) / B_total * 100
   ```

4. **Decision de parada**. Si el mejor individuo de la generacion alcanza el
   fitness objetivo (100% de cobertura), el ciclo termina y se reporta el
   individuo.

5. **Seleccion por torneo** (`selection.py`, Sec. 3.4). Se eligen dos padres
   comparando subconjuntos aleatorios de la poblacion por fitness.

6. **Crossover de un punto** (`crossover.py`, Sec. 3.2.1). Los dos padres se
   combinan generando dos hijos, intercambiando los genes posteriores a un
   punto de corte aleatorio.

7. **Mutacion por reordenamiento** (`mutation.py`, Sec. 3.2.2). Los genes de
   los hijos se reordenan al azar, sin alterar su contenido.

8. **Nueva generacion**. Los hijos reemplazan a los individuos de menor
   fitness de la poblacion actual (elitismo simple); el ciclo vuelve al
   paso 2.

## Ejemplo de corrida documentada (`--seed 32`)

El archivo `ejemplo_ejecucion.txt` contiene el log completo de correr
`python3 main.py --seed 32`. El resultado mas relevante ocurre en la
Generacion 3:

```
Padre 1: {'nombre': 'Alice', 'edad': 70, 'rol': 'admin'}
    cubre B1, B2, B4  (75%)
Padre 2: {'activo': False, 'nombre': 'Alice', 'edad': 70}
    cubre B1, B2, B3  (75%)

Crossover de un punto -> Hijo 2:
    {'activo': False, 'nombre': 'Alice', 'edad': 70, 'rol': 'admin'}
    cubre B1, B2, B3, B4  (100%)
```

Ningun padre por si solo cubria las 4 ramas. El crossover combino el gen
`activo` del Padre 2 con el gen `rol` del Padre 1, generando un individuo que
alcanza cobertura total en la Generacion 4. Esto ilustra exactamente lo que
el paper argumenta en la Seccion 4.2 sobre por que el crossover es
indispensable: sin el, un algoritmo que solo muta (como el benchmark
EvoGFuzz que compara el paper) queda limitado a variaciones locales de un
mismo individuo y no puede combinar genes de dos individuos distintos.

## Una limitacion real observada (semilla por defecto, sin `--seed`)

En corridas donde la poblacion inicial pierde tempranamente el gen `activo`,
el algoritmo puede converger en 75% de cobertura sin alcanzar el 100%,
porque el operador de mutacion usado (reorder) reordena genes existentes
pero no introduce genes nuevos que ya se hayan perdido de toda la poblacion.
Esto no es un error de la implementacion: es consistente con el diseno del
paper, que separa explicitamente los roles de cada operador (Sec. 4.2): el
crossover es responsable de la exploracion de combinaciones nuevas, mientras
que la mutacion aporta ajustes finos (*exploitation*) sobre el material
genetico ya presente en la poblacion.

Para ver esta limitacion en vivo, corre `python3 main.py` varias veces sin
`--seed` y observa que algunas corridas terminan en 75% al llegar al maximo
de generaciones en vez de en 100%.

## Troubleshooting

- **`python3: command not found`**: en algunos sistemas el binario se llama
  `python` en vez de `python3`. Probar `python --version`; si es 3.x, usar
  ese comando.
- **La salida de `--seed 32` no coincide con `ejemplo_ejecucion.txt`**: la
  version de Python no deberia afectar el resultado (no se usan librerias
  externas ni orden de diccionarios dependiente de la version), pero si
  ocurre, correr `python3 --version` y reportarlo — el algoritmo de
  `random` con semilla fija es determinista dentro de la misma version
  mayor de Python 3.
