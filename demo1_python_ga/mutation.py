"""
mutation.py

Reorder mutation (paper Sec. 3.2.2, Fig. 3). Reordena claves sin
tocar valores; el paper la prefirio a eliminar/anidar campos porque
nunca produce un JSON invalido.
"""

import random


def mutacion_reorder(individuo: dict) -> dict:
    """Reordena al azar las claves (genes) de un individuo, mismo contenido."""
    claves = list(individuo.keys())
    random.shuffle(claves)
    return {clave: individuo[clave] for clave in claves}
