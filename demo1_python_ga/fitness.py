"""
fitness.py

Fitness = branch coverage (paper Sec. 3.3, Ecuacion 1):

    Fitness(x) = B_exec(x) / B_total * 100
"""

from sut import run_sut, TOTAL_BRANCHES, NOMBRES_RAMAS


def fitness(individuo: dict) -> float:
    """Calcula Fitness(x) segun la Ecuacion 1 del paper."""
    cubiertas = run_sut(individuo)
    b_exec = sum(cubiertas)
    return (b_exec / TOTAL_BRANCHES) * 100


def ramas_cubiertas(individuo: dict) -> list:
    """Devuelve el nombre de las ramas que cubre un individuo (para logging)."""
    cubiertas = run_sut(individuo)
    return [nombre for nombre, c in zip(NOMBRES_RAMAS, cubiertas) if c]
