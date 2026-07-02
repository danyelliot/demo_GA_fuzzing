"""
selection.py

Tournament selection (paper Sec. 3.4). El paper no fija el tamanio
del torneo; k=3 es el valor tipico en la literatura de AGs.
"""

import random

from fitness import fitness


def seleccion_por_torneo(poblacion: list, k: int = 3) -> dict:
    """
    Toma k individuos al azar de la poblacion y devuelve el de
    mayor fitness. A diferencia de la ruleta, no garantiza que gane
    el mejor global: solo compite dentro de su subconjunto.
    """
    k = min(k, len(poblacion))
    candidatos = random.sample(poblacion, k)
    ganador = max(candidatos, key=fitness)
    return ganador
