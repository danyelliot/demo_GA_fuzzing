"""
crossover.py

One-point crossover (paper Sec. 3.2.1, Fig. 2). El paper prefiere
one-point sobre two-point/uniform porque preserva mejor las
relaciones estructurales dentro del JSON.
"""

import random


def cruce_un_punto(padre1: dict, padre2: dict) -> tuple:
    """
    Cruce de un punto entre dos padres (dicts). El "punto de corte"
    se toma sobre la lista de claves de cada padre: se elige un
    indice de corte por padre y se intercambian las claves
    posteriores a ese indice. Devuelve (hijo1, hijo2).
    """
    claves1 = list(padre1.keys())
    claves2 = list(padre2.keys())

    if not claves1 or not claves2:
        return dict(padre1), dict(padre2)

    punto1 = random.randint(1, len(claves1))
    punto2 = random.randint(1, len(claves2))

    hijo1 = {clave: padre1[clave] for clave in claves1[:punto1]}
    hijo1.update({clave: padre2[clave] for clave in claves2[punto2:]})

    hijo2 = {clave: padre2[clave] for clave in claves2[:punto2]}
    hijo2.update({clave: padre1[clave] for clave in claves1[punto1:]})

    return hijo1, hijo2
