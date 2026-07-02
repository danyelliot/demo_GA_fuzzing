"""
main.py

Orquesta el ciclo evolutivo completo (paper Fig. 1, Sec. 3):

    Poblacion inicial (3.1) -> ejecutar contra el SUT -> fitness (3.3)
        -> fitness suficiente? SI: stop / NO: seleccion (3.4)
        -> crossover (3.2.1) -> mutacion (3.2.2) -> nueva generacion

Uso:
    python main.py
    python main.py --seed 32     # reproduce el log de ejemplo_ejecucion.txt
"""

import argparse
import random

from population import generar_poblacion_inicial
from fitness import fitness, ramas_cubiertas
from selection import seleccion_por_torneo
from crossover import cruce_un_punto
from mutation import mutacion_reorder

TAMANIO_POBLACION = 6
GENERACIONES_MAXIMAS = 5
FITNESS_OBJETIVO = 100.0  # 100% de branch coverage (Seccion 3.3)


def imprimir_individuo(etiqueta: str, individuo: dict) -> None:
    f = fitness(individuo)
    ramas = ramas_cubiertas(individuo) or ["ninguna"]
    print(f"  {etiqueta}: {individuo}")
    print(f"      fitness = {f:.1f}%  |  ramas cubiertas = {', '.join(ramas)}")


def correr_ciclo_evolutivo() -> None:
    print("=" * 72)
    print("PASO 1 - Poblacion inicial (Seccion 3.1 del paper, cold-start)")
    print("=" * 72)
    poblacion = generar_poblacion_inicial(TAMANIO_POBLACION)
    for i, ind in enumerate(poblacion, start=1):
        imprimir_individuo(f"Individuo {i}", ind)

    for gen in range(1, GENERACIONES_MAXIMAS + 1):
        print("\n" + "=" * 72)
        print(f"GENERACION {gen}")
        print("=" * 72)

        mejor = max(poblacion, key=fitness)
        mejor_fitness = fitness(mejor)
        print(f"Mejor fitness de la generacion actual: {mejor_fitness:.1f}%")

        # rombo "Decision" de la Figura 1 del paper
        if mejor_fitness >= FITNESS_OBJETIVO:
            print("\nCriterio de parada alcanzado: 100% de branch coverage.")
            print(f"Individuo que logro cobertura total: {mejor}")
            return

        print("\nPASO 2 - Seleccion por torneo (Seccion 3.4)")
        padre1 = seleccion_por_torneo(poblacion)
        padre2 = seleccion_por_torneo(poblacion)
        imprimir_individuo("Padre 1", padre1)
        imprimir_individuo("Padre 2", padre2)

        print("\nPASO 3 - Crossover de un punto (Seccion 3.2.1, Figura 2)")
        hijo1, hijo2 = cruce_un_punto(padre1, padre2)
        imprimir_individuo("Hijo 1 (antes de mutar)", hijo1)
        imprimir_individuo("Hijo 2 (antes de mutar)", hijo2)

        print("\nPASO 4 - Mutacion por reordenamiento (Seccion 3.2.2, Figura 3)")
        hijo1 = mutacion_reorder(hijo1)
        hijo2 = mutacion_reorder(hijo2)
        imprimir_individuo("Hijo 1 (mutado)", hijo1)
        imprimir_individuo("Hijo 2 (mutado)", hijo2)

        print("\nPASO 5 - Nueva generacion (reemplazo con elitismo simple)")
        # Los 2 individuos de menor fitness se reemplazan por los hijos;
        # el resto sobrevive. Estrategia de reemplazo no fijada por el
        # paper, adoptada aqui para mantener el tamanio de poblacion fijo.
        poblacion_ordenada = sorted(poblacion, key=fitness, reverse=True)
        sobrevivientes = poblacion_ordenada[:-2]
        poblacion = sobrevivientes + [hijo1, hijo2]

        for i, ind in enumerate(poblacion, start=1):
            imprimir_individuo(f"Individuo {i}", ind)

    print("\nSe alcanzo el numero maximo de generaciones sin cobertura total.")
    mejor = max(poblacion, key=fitness)
    print(f"Mejor individuo final: {mejor}  (fitness = {fitness(mejor):.1f}%)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Corre el ciclo del Algoritmo Genetico del paper (arXiv:2508.05923) "
                    "sobre el SUT de ejemplo."
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="Semilla para random, util para reproducir una corrida exacta "
             "(ej: --seed 32 reproduce el ejemplo documentado en el README)."
    )
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)
        print(f"[semilla fijada en {args.seed} para reproducibilidad]\n")

    correr_ciclo_evolutivo()
